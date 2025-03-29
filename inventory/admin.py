from django.contrib import admin

# Register your models here.
from .models import Supplier,Warehouse,Inventory

admin.site.register(Supplier)
admin.site.register(Warehouse)
admin.site.register(Inventory)
