from django.db import models
from inventory.models import Inventory, Warehouse
from franchise.models import User

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id}"


class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shipment for Order {self.order.id}"


class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=50, choices=DELIVERY_STATUS_CHOICES)
    delivery_date = models.DateTimeField()

    def __str__(self):
        return f"Delivery for Order {self.order.id}"
