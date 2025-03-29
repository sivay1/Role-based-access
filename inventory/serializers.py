from rest_framework import serializers
from .models import Supplier, Warehouse, Inventory
from django.core.validators import MinValueValidator


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
   quantity = serializers.IntegerField(validators=[MinValueValidator(1)]) 
   supplier = SupplierSerializer(read_only=True)
   warehouse = WarehouseSerializer(read_only=True)
   supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), write_only=True)
   warehouse_id = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), write_only=True)

   class Meta:
        model = Inventory
        fields = '__all__'
   def create(self, validated_data):
        supplier = validated_data.pop('supplier_id')
        warehouse = validated_data.pop('warehouse_id')
        inventory = Inventory.objects.create(supplier=supplier, warehouse=warehouse, **validated_data)
        return inventory
   
   def update(self, instance, validated_data):
        # Handle supplier_id and warehouse_id during updates
        supplier = validated_data.pop('supplier_id', None)
        warehouse = validated_data.pop('warehouse_id', None)
        
        if supplier:
            instance.supplier = supplier
        if warehouse:
            instance.warehouse = warehouse

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
