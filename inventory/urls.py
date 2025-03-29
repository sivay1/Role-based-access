from django.urls import path
from .  import views
from inventory.views import(
     WarehouseListCreateAPIView,WarehouseDetailAPIView,warehouses,InventoryListCreateAPIView,
     InventoryDetailAPIView,inventory,create_inventory,SupplierListCreateAPIView,SupplierDetailAPIView,
     suppliers
)
urlpatterns = [
     # Warehouse URLs
    path('api/warehouses-view/', WarehouseListCreateAPIView.as_view(), name='warehouse-list-create'),
    path('warehouses/', views.warehouses, name='warehouses'),
    path('api/warehouses/<int:pk>/', WarehouseDetailAPIView.as_view(), name='warehouse-detail'),
    path('warehouse-create/', WarehouseListCreateAPIView.as_view(), name='create_warehouse_view'),
    path('warehouse/create/', views.create_warehouse, name='create_warehouse'),

    #Inventory URLs
    path('api/inventory-view/', InventoryListCreateAPIView.as_view(), name='inventory-list'),
    path('inventory/', views.inventory, name='inventory'),
    path('api/inventory-create/', InventoryListCreateAPIView.as_view(), name='create_inventory_view'),
    path('inventory/create/', views.create_inventory, name='create_inventory'),
    path('api/inventory-update/<int:pk>/', InventoryDetailAPIView.as_view(), name='update_inventory_view'),
    path('inventory/update/<int:pk>/', views.update_inventory, name='update_inventory'),
    path('api/inventory/delete/<int:pk>/', InventoryDetailAPIView.as_view(), name='delete_inventory_view'),
    path('inventory_delete/<int:pk>/', views.delete_inventory, name='delete_inventory'),
    #Supplier URLs
    path('api/suppliers-view/', SupplierListCreateAPIView.as_view(), name='supplier-list-create'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('api/suppliers/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier-detail'),
    path('api/supplier-create/', SupplierListCreateAPIView.as_view(), name='supplier-list-create'),
    path('suppliers/create/', views.create_supplier, name='create_suppliers'),
    
    path('export_reports/<str:report_type>/', views.export_reports, name='export_reports'),
    path('upload_inventory/', views.upload_inventory, name='uploadinventory'),
    
    
    path('sales/', views.sales, name = "sales"),
    path('sales-graph/', views.sales_graph, name='sales_graph'),
#     path('sales/add/', views.add_sales, name='add_sales'),
    
    path('billing/', views.billing, name = "billing"),
    path('billing-graph/', views.billing_graph, name='billing_graph'),
    path('billing/add/', views.add_billing, name='add_billing'),

    path('audit-logs/', views.audit_logs, name='audit_logs'),


   
]