from django.contrib import admin
from .models import Address, Blog, Category, Product, Cart, Order, OrderItem, Coupon
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .utils import send_delivery_email

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'pincode')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('address', 'city', 'state', 'pincode')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')
    
    def save_model(self, request, obj, form, change):
        if change:
            previous = Order.objects.get(pk=obj.pk)
            if previous.status != obj.status and obj.status == 'Delivered':
                send_delivery_email(obj.user.email, obj.product.title ,obj.id)
        super().save_model(request, obj, form, change)

class CustomUserAdmin(UserAdmin):
    def verified_status(self, obj):
        return "✅ Verified" if obj.is_active else "❌ Not Verified"
    
    verified_status.short_description = "Verification Status"

    list_display = ('username', 'email', 'verified_status', 'date_joined')
    list_filter = ['is_active']  

    search_fields = ('username', 'email')
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'usage_limit', 'used_count', 'is_active']
    list_filter = ['is_active', 'discount_type']
    search_fields = ['code']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Blog)