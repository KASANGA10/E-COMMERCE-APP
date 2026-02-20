from django.contrib import admin
from .models import Shop, Manager, Category, Brand, Product, ProductImage

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'registration_date')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price', 'stock', 'status')