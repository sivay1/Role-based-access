from django.urls import path
from logistics import views
from logistics.views import(
    OrderListCreateAPIView,OrderDetailAPIView,ShipmentListCreateAPIView,DeliveryListCreateAPIView,
    orders,create_order,update_order,delete_order,shipments,deliveries
)


urlpatterns = [
    path('api/orders-view/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('orders/', views.orders, name='orders'),
    path('api/order-create/', OrderListCreateAPIView.as_view(), name='create_order_view'),
    path('orders/create/', views.create_order, name='create_order'),
    path('api/orders-update/<int:pk>/', OrderDetailAPIView.as_view(), name='update_order_view'),
    path('order_update/<int:pk>/', views.update_order, name='update_order'),
    path('api/orders/delete/<int:pk>/', OrderDetailAPIView.as_view(), name='delete_order_view'),
    path('orders_delete/<int:pk>/', views.delete_order, name='delete_order'),

    path('api/shipments-view/', ShipmentListCreateAPIView.as_view(), name='shipment-list-create'),
    path('shipments/', views.shipments, name='shipments'),
    
    path('api/delivery-view/', DeliveryListCreateAPIView.as_view(), name='delivery-list-create'),
    path('deliveries/', views.deliveries, name='deliveries'),
]