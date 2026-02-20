from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, ProductViewSet, ShopViewSet, VendorOrderViewSet



# The router automatically generates URL patterns for the ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'vendor-orders', VendorOrderViewSet, basename='vendor-order')

app_name = 'shop'

urlpatterns = [
    # This includes the auto-generated URLs (e.g., /products/, /products/1/, /shops/)
    path('', include(router.urls)),
]