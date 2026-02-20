from rest_framework import serializers
from .models import Shop, Product, ProductImage, Cart,CartItem, Category, Order, ShopOrder, OrderDetail

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_feature', 'alt_text']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'slug', 'description', 'status']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    shop_name = serializers.ReadOnlyField(source='shop.name')

    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'shop_name', 'category', 'name', 
            'description', 'price', 'stock', 'images'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())




class OrderDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class ShopOrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, read_only=True)
    shop_name = serializers.ReadOnlyField(source='shop.name')

    class Meta:
        model = ShopOrder
        fields = ['id', 'shop', 'shop_name', 'items', 'status', 'shop_total']

class OrderSerializer(serializers.ModelSerializer):
    shop_orders = ShopOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_amount', 'status', 'shop_orders']