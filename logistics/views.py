from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required(login_url='login')
# def orders_view(request):
#     return render(request,"logistics/orders.html")

from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.models import User
from logistics.models import Delivery,Shipment,Order

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from logistics.serializers import OrderSerializer,DeliverySerializer,ShipmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from rest_framework.permissions import IsAuthenticated, AllowAny
# from franchise.serializers import *
from logistics.permissions import IsAdmin, IsFranchiseOwner, IsCustomerSupport,IsLogisticsPersonnel,IsManager
from rest_framework.authtoken.models import Token


# from .models import Supplier, Warehouse
# from .serializers import SupplierSerializer, WarehouseSerializer

from .permissions import IsAdmin, IsManager  # Assuming these permissions are defined
import requests
from franchise.models import Role


class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & IsAdmin]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated & IsAdmin]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        order = self.get_object(pk)
        if order:
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        

        return Response({"message": "Order not found"},status=status.HTTP_404_NOT_FOUND)
    
class ShipmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager)]

    def get(self, request):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomerSupport | IsAdmin)]

    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

BASE_URL = "http://127.0.0.1:8000"

def orders(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/orders-view/', headers=headers)
    

    if response.status_code == 200:
        orders = response.json()
        return render(request, 'logistics/orders.html', {'orders': orders})
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'logistics/orders.html', {'error': 'Failed to fetch orders'})
def create_order(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found
    owner_role = Role.objects.filter(name="Franchise Owner").first()
    owners = User.objects.filter(profile__role=owner_role)

    if request.method == 'POST':
        data = {
            'customer': request.POST.get('customer'),
            'inventory': request.POST.get('inventory'),
            'order_date': request.POST.get('order_date'),
            'order_status': request.POST.get('order_status')
        }
        headers = {
            'Authorization': f'Token {token}'
        }
        response = requests.post(f'{BASE_URL}/api/order-create/', json=data, headers=headers)
        print("API Response:", response.status_code, response.json())
        
        if response.status_code == 201:
            messages.success(request, "Order added.")
            return redirect('orders')  # Redirect to orders page after successful creation
        else:
            return render(request, 'create_order.html', {'error': response.json()})
    
    return render(request, 'create_order.html',{'owners':owners})


def update_order(request, pk):
    token = request.session.get('auth_token')
    
    if not token:
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type' : 'application/json'

    }
    if request.method == 'POST':
        data = {
            'customer': request.POST.get('customer'),
            'inventory': request.POST.get('inventory'),
            'order_date': request.POST.get('order_date'),
            'order_status': request.POST.get('order_status')
        }
        response = requests.put(f'{BASE_URL}/api/orders-update/{pk}/', json=data, headers=headers)
        print("PUT Response Status Code:", response.status_code)
        
        if response.status_code == 200:
            messages.success(request, "Update success.")
            return redirect('orders')  # Redirect to orders page after successful update
            
        else:
            return render(request, 'logistics/update_order.html', {'error': response.json()})
    
    # Fetch the order details for pre-filling the form
    response = requests.get(f'{BASE_URL}/api/orders-update/{pk}/', headers=headers)
    print("GET Response Status Code:", response.status_code)
    # if response.status_code == 200:
    #     order = response.json()
    #     return render(request, 'update_order.html', {'order': order})
    # else:
    #     return redirect('orders')
    if response.status_code == 200:
        try:
            order = response.json()
            return render(request, 'logistics/update_order.html', {'order': order})
        except requests.exceptions.JSONDecodeError:
            return render(request, 'logistics/update_order.html', {'error': 'Invalid JSON response from API'})
    else:
        return redirect('logistics/orders')
    
def delete_order(request, pk):
    token = request.session.get('auth_token')
    if not token:
        print("No token")
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'
    }
    print(f"Delete viw Token: {token}")  # Debugging
    print(f"delete view Headers: {headers}") 
    response = requests.delete(f'{BASE_URL}/api/orders/delete/{pk}/', headers=headers)
    
    if response.status_code == 204:
        try:
            return redirect('orders')  # Redirect to orders page after successful deletion
        except Exception as e:
            print(e)
    else:
        return render(request, 'logistics/orders.html', {'error': 'Failed to delete order'})
    
def shipments(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/shipments-view/', headers=headers)
    
    if response.status_code == 200:
        shipments = response.json()
        return render(request, 'logistics/shipments.html', {'shipments': shipments})
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'logistics/shipments.html', {'error': 'Failed to fetch shipments'})

def deliveries(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/delivery-view/', headers=headers)
    
    if response.status_code == 200:
        deliveries = response.json()
        return render(request, 'logistics/deliveries.html', {'deliveries': deliveries})
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'logistics/deliveries.html', {'error': 'Failed to fetch deliveries'})