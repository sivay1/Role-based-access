# from django import forms
# from .models import Supplier,Warehouse

# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ['supplier_name', 'contact_info']

# class WarehouseForm(forms.ModelForm):
#     class Meta:
#         model = Warehouse
#         fields = ['warehouse_location','manager']
from django import forms
from .models import Billing,Sales

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['order', 'payment_method', 'amount', 'is_paid']
       

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['product', 'quantity_sold', 'sale_date', 'customer']
        widgets = {
            'sale_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }