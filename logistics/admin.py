from django.contrib import admin

# Register your models here.
from . models import Order,Shipment,Delivery

admin.site.register(Order)
admin.site.register(Shipment)
admin.site.register(Delivery)
