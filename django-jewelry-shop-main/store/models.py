from datetime import timedelta
import decimal
from django.utils import timezone

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.TextField(default="")
    user_phone_number = models.CharField(max_length=10,default="")
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,default="")
    pincode = models.CharField(max_length=10,default="") 

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} - {self.pincode}, {self.user_phone_number}"


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
      

    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Order(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]
    
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount",default=0)   
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=99.00)  
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    razorpay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razorepay_payment_signature = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')  # New field
    payment_status = models.CharField(max_length=20, default='Pending')  # Optional field
    tracking_uid = models.CharField(max_length=100, unique=True, blank=True, null=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )
    
    
    def __str__(self):
        return f"{self.user} - {self.product} ({self.status})"
    
    def save(self, *args, **kwargs):
        if not self.tracking_uid:
            self.tracking_uid = str(uuid.uuid4()).replace('-', '')[:10]
            
        if not self.estimated_delivery:
            self.estimated_delivery = self.ordered_date + timedelta(days=6) if self.ordered_date else timezone.now() + timedelta(days=6)
            
        if self.product and self.quantity:
            self.amount = self.quantity * self.product.price
        else:
            self.amount = 0
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    
    @property
    def subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())
    
    @property
    def products_list(self):
        return ", ".join([str(item.product) for item in self.orderitem_set.all()])

        
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
from django.utils.text import slugify
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog_images/')
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# New Coupon Model
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(
    max_length=10,
    choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')],
    default='percentage'
)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to and self.used_count < self.usage_limit

    def get_discount_amount(self, total_amount):
        if self.discount_type == 'percentage':
            return (self.discount_value / 100) * total_amount
        elif self.discount_type == 'fixed':
            return self.discount_value
        return decimal.Decimal(0)

    def __str__(self):
        return self.code