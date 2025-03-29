from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_info = models.TextField()
    address = models.TextField(default="address")  # Supplier's address  
    city = models.CharField(max_length=100,default="city")  # City  
    state = models.CharField(max_length=100, blank=True, null=True)  # State/Province  
    country = models.CharField(max_length=100, default="India")  # Country  
    pincode = models.CharField(max_length=10, blank=True, null=True)  # ZIP code  


    def __str__(self):
        return self.supplier_name


class Warehouse(models.Model):
    warehouse_location = models.CharField(max_length=255)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.warehouse_location


class Inventory(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(1.00)])
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Billing(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]
    order = models.ForeignKey('logistics.Order', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Billing for Order {self.order.id}"

class Sales(models.Model):
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sale_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.product.product_name} on {self.sale_date}"
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    details = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} {self.action}d {self.model_name} at {self.timestamp}"