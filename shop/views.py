from rest_framework import viewsets, permissions, status
from .serializers import OrderSerializer, ProductSerializer, ShopSerializer, CartSerializer,ShopOrderSerializer, CartItemSerializer
from .permissions import IsShopManager
from .models import Cart, CartItem, Product, Shop, Order, ShopOrder, OrderDetail
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles viewing products (Public) and editing (Managers Only).
    """
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Allow anyone to view list/detail, but require manager for changes
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsShopManager()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Automatically set the product's shop to the manager's assigned shop
        serializer.save(shop=self.request.user.manager_profile.shop)

class ShopViewSet(viewsets.ModelViewSet):
    """
    Handles viewing shops (Public) and editing shop profile (Managers Only).
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        # Only the manager of a specific shop should be able to edit that shop
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsShopManager()]
        return [permissions.AllowAny()]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Using get_or_create ensures the user always has a cart object
        Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            quantity = int(request.data.get('quantity', 1))
            product = Product.objects.get(id=product_id)
        except (Product.DoesNotExist, TypeError, ValueError):
            return Response({"error": "Valid Product ID and Quantity required"}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')
        try:
            item = CartItem.objects.get(cart__user=request.user, product_id=product_id)
            item.delete()
            return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # 1. Create Parent Order
            main_order = Order.objects.create(
                user=request.user,
                total_amount=0, 
                status='pending'
            )

            total_amount = 0
            shop_orders = {}

            # 2. Process items and group by Shop
            for item in cart_items:
                product = item.product
                shop = product.shop
                line_total = item.quantity * product.price

                if shop.id not in shop_orders:
                    shop_orders[shop.id] = ShopOrder.objects.create(
                        main_order=main_order,
                        shop=shop,
                        shop_total=0,
                        status='pending'
                    )

                # 3. Create OrderDetail (Line Item)
                OrderDetail.objects.create(
                    order=main_order,
                    shop_order=shop_orders[shop.id],
                    product=product,
                    quantity=item.quantity,
                    price=product.price
                )

                # Update running totals
                shop_orders[shop.id].shop_total += line_total
                total_amount += line_total

            # 4. Save ShopOrder totals and Main Order total
            for s_order in shop_orders.values():
                s_order.save()

            main_order.total_amount = total_amount
            main_order.save()

            # 5. Clear Cart
            cart_items.delete()

        return Response({
            "message": "Order created successfully",
            "order_id": main_order.id,
            "total_amount": main_order.total_amount,
            "shop_orders_count": len(shop_orders)
        }, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users can view their own order history and specific order details.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'shop_orders__items', 
            'shop_orders__shop'
        )

class VendorOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Shop Managers to manage orders specific to their shop.
    """
    serializer_class = ShopOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter shop orders by the shop owned/managed by the current user
        return ShopOrder.objects.filter(shop__manager_profile__user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Custom action to allow managers to move an order from PENDING to COMPLETED/SHIPPED.
        """
        shop_order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in [choice[0] for choice in shop_order._meta.get_field('status').choices]:
            shop_order.status = new_status
            shop_order.save()
            return Response({'status': 'order status updated'})
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)