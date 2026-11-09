from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5  

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  
    readonly_fields = ['product_title', 'price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'phone', 'delivery_service', 'paid', 'created_at']
    list_filter = ['paid', 'delivery_service', 'created_at']
    search_fields = ('first_name', 'phone', 'city')
    inlines = [OrderItemInline]

admin.site.register(Product)