from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from inventory.models import Warehouse,Inventory,Supplier,AuditLog
from django.contrib import messages

from inventory.serializers import WarehouseSerializer,InventorySerializer,SupplierSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from inventory.permissions import IsAdmin, IsFranchiseOwner, IsCustomerSupport,IsLogisticsPersonnel,IsManager
from rest_framework.authtoken.models import Token
from .permissions import IsAdmin, IsManager
import requests
from franchise.models import Role
import json,csv
from .forms import BillingForm,SalesForm
from django.core.paginator import Paginator
from inventory.audit import log_action

class SupplierListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsFranchiseOwner)]  # Allow Admin or Manager

    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierDetailAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager |IsFranchiseOwner)]  # Allow Admin or Manager

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return None

    def get(self, request, pk):
        supplier = self.get_object(pk)
        if supplier:
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        supplier = self.get_object(pk)
        if supplier:
            serializer = SupplierSerializer(supplier, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        supplier = self.get_object(pk)
        if supplier:
            supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class WarehouseListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsFranchiseOwner)]  # Allow Admin or Manager

    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager |IsFranchiseOwner)]  # Allow Admin or Manager

    def get_object(self, pk):
        try:
            return Warehouse.objects.get(pk=pk)
        except Warehouse.DoesNotExist:
            return None

    def get(self, request, pk):
        warehouse = self.get_object(pk)
        if warehouse:
            serializer = WarehouseSerializer(warehouse)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        warehouse = self.get_object(pk)
        if warehouse:
            serializer = WarehouseSerializer(warehouse, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        warehouse = self.get_object(pk)
        if warehouse:
            warehouse.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class InventoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsFranchiseOwner)]  # Allow Admin or Manager

    def get(self, request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsFranchiseOwner)]  # Allow Admin or Manager

    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return None

    def get(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            serializer = InventorySerializer(inventory)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            serializer = InventorySerializer(inventory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            inventory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

BASE_URL = "http://127.0.0.1:8000"
def suppliers(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_view')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/suppliers-view/', headers=headers)
    
    if response.status_code == 200:
        suppliers = response.json()
        return render(request, 'inventory/suppliers.html', {'suppliers': suppliers})
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'inventory/suppliers.html', {'error': 'Failed to fetch suppliers'})
    
def create_supplier(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found
    # owner_role = Role.objects.filter(name="Franchise Owner").first()
    # owners = User.objects.filter(profile__role=owner_role)

    if request.method == 'POST':
        data = {
            'supplier_name': request.POST.get('supplier_name'),
            'contact_info' : request.POST.get('contact_info'),   
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            
            'pincode': request.POST.get('pincode'),
        }
        headers = {
            'Authorization': f'Token {token}'
        }
        response = requests.post(f'{BASE_URL}/api/supplier-create/', json=data, headers=headers)
        print("API Response:", response.status_code, response.json())
        
        if response.status_code == 201:
            messages.success(request, "Supplier added.")
            return redirect('suppliers')  # Redirect to suppliers page after successful creation
        else:
            return render(request, 'create_supplier.html', {'error': response.json()})
    
    return render(request, 'create_supplier.html')

    
def warehouses(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/warehouses-view/', headers=headers)
    
    if response.status_code == 200:
        warehouses = response.json()
        return render(request, 'inventory/warehouses.html', {'warehouses': warehouses})
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'inventory/warehouses.html', {'error': 'Failed to fetch warehouses'})

def create_warehouse(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found

    manager_role = Role.objects.filter(name="Manager").first()
    managers = User.objects.filter(profile__role=manager_role)

    if request.method == 'POST':
        data = {
            'warehouse_location': request.POST.get('warehouse_location'),
            'manager': request.POST.get('manager')
        }
        headers = {
            'Authorization': f'Token {token}'
        }
        response = requests.post(f'{BASE_URL}/api/warehouse-create/', json=data, headers=headers)
        print("API Response:", response.status_code, response.json())
        
        if response.status_code == 201:
            messages.success(request, "Warehouse added.")
            return redirect('warehouses')  # Redirect to orders page after successful creation
        else:
            return render(request, 'create_warehouse.html', {'error': response.json()})
    
    return render(request, 'create_warehouse.html',{'managers': managers})

def inventory(request):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'  # Include the token in the headers
    }
    
    print("Headers Sent:", headers)  # Debugging line
    response = requests.get(f'{BASE_URL}/api/inventory-view/', headers=headers)
    
    if response.status_code == 200:
        inventory = response.json()
        return render(request, 'inventory/inventory.html', {'inventory': inventory})
    
    else:
        print("API Response:", response.status_code, response.json())  # Debug: Check the API response
        return render(request, 'inventory/inventory.html', {'error': 'Failed to fetch inventory'})

def create_inventory(request):
    token = request.session.get('auth_token')
    if not token:
        messages.error(request, "Error authentication token not found")
        return redirect('login_user')  # Redirect to login if no token is found
    
    headers = {
            'Authorization': f'Token {token}'
    }
    suppliers_response = requests.get(f'{BASE_URL}/api/suppliers-view/', headers=headers)
    warehouses_response = requests.get(f'{BASE_URL}/api/warehouses-view/', headers=headers)

    suppliers = suppliers_response.json() if suppliers_response.status_code == 200 else []
    warehouses = warehouses_response.json() if warehouses_response.status_code == 200 else []
    if request.method == 'POST':
        data = {
            'product_name': request.POST.get('product_name'),
            'quantity': request.POST.get('quantity'),
            'price' : request.POST.get('price'),
            'supplier_id': request.POST.get('supplier'),
            'warehouse_id':request.POST.get('warehouse')
        }

        response = requests.post(f'{BASE_URL}/api/inventory-create/', json=data, headers=headers)
        print("API Response:", response.status_code)
        print("GET Response Status Code:", response.status_code)
        if response.status_code == 201:
            messages.success(request, "Item added to inventory.")
            return redirect('inventory')  # Redirect to orders page after successful creation
        else:
            return render(request, 'create_inventory.html', {
                'error': response.json(),
                'suppliers': suppliers,
                'warehouses': warehouses,
            })
    
    return render(request, 'create_inventory.html', {
                'suppliers': suppliers,
                'warehouses': warehouses,
            })

def update_inventory(request, pk):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'
    }

    # Fetch suppliers and warehouses from the API
    suppliers_response = requests.get(f'{BASE_URL}/api/suppliers-view/', headers=headers)
    warehouses_response = requests.get(f'{BASE_URL}/api/warehouses-view/', headers=headers)

    suppliers = suppliers_response.json() if suppliers_response.status_code == 200 else []
    warehouses = warehouses_response.json() if warehouses_response.status_code == 200 else []

    if request.method == 'POST':
        data = {
            'product_name': request.POST.get('product_name'),
            'quantity': request.POST.get('quantity'),
            'supplier_id': request.POST.get('supplier'),
            'warehouse_id': request.POST.get('warehouse')
        }
        response = requests.put(f'{BASE_URL}/api/inventory-update/{pk}/', json=data, headers=headers)
        
        if response.status_code == 200:
            messages.success(request, "Update success!.")
            return redirect('inventory')  # Redirect to inventory list after successful update
        else:
            return render(request, 'inventory/update_inventory.html', {
                'error': response.json(),
                'suppliers': suppliers,
                'warehouses': warehouses,
                'inventory': {'id': pk, **data}  # Pass form data back to the template
            })
    
    # Fetch the inventory details for pre-filling the form
    response = requests.get(f'{BASE_URL}/api/inventory-update/{pk}/', headers=headers)
    if response.status_code == 200:
        inventory = response.json()
        return render(request, 'inventory/update_inventory.html', {
            'inventory': inventory,
            'suppliers': suppliers,
            'warehouses': warehouses
        })
    else:
        return redirect('inventory')

def delete_inventory(request, pk):
    token = request.session.get('auth_token')
    if not token:
        return redirect('login_user')  # Redirect to login if no token is found

    headers = {
        'Authorization': f'Token {token}'
    }
    print(f"Delete view Token: {token}")  # Debugging
    print(f"delete view Headers: {headers}") 
    
    # First get the inventory item details before deleting
    get_response = requests.get(f'{BASE_URL}/api/inventory-update/{pk}/', headers=headers)
    
    if get_response.status_code == 200:
        inventory = get_response.json()
        product_name = inventory.get('product_name', 'Unknown Product')
        
        
        response = requests.delete(f'{BASE_URL}/api/inventory/delete/{pk}/', headers=headers)
        
        if response.status_code == 204:
            # Log the deletion
            log_action(
                user=request.user,
                action='DELETE',
                model_name='Inventory',
                object_id=pk,
                details=f"Deleted inventory item: {product_name}"
            )
            messages.success(request, "Inventory item deleted successfully.")
            return redirect('inventory')
        else:
            messages.error(request, "Failed to delete inventory item.")
            return render(request, 'inventory.html', {'error': 'Failed to delete inventory item'})
    else:
        messages.error(request, "Inventory item not found.")
        return redirect('inventory')

def export_reports(request, report_type):
    if 'auth_token' not in request.session:  # Check if user is authenticated
        return redirect('login_user')
    elif report_type == "json":
        data = {
            "inventory": list(Inventory.objects.values()),
        }
        response = HttpResponse(json.dumps(data), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename="report.json"'
        return response

    elif report_type == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        writer = csv.writer(response)
        writer.writerow(["product_name","quantity","price","supplier","warehouse" ])

        for item in Inventory.objects.all():
            writer.writerow([item.product_name, item.quantity, item.price, item.supplier, item.warehouse])

        return response
    else:
        return HttpResponse("Invalid report type", status=400)
    

def upload_inventory(request):
    item_added = 0
    if 'auth_token' not in request.session:  
        return redirect('login_user')

    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Invalid file format! Please upload a CSV file.")
            return redirect('upload_inventory')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file, delimiter=',')

        next(reader)  # Skip header row

        for row in reader:
            try:
                if len(row) != 5:  # Check if row has exactly 4 values
                    print(f"Skipping row {row}: not enough values")
                    continue  # Skip the row and move to the next one
                product_name, quantity, price, supplier_name, warehouse_location = [value.strip() for value in row]

                # Check if supplier & warehouse exist
                supplier = Supplier.objects.filter(supplier_name=supplier_name).first()
                warehouse = Warehouse.objects.filter(warehouse_location=warehouse_location).first()

                if not supplier or not warehouse:
                    messages.error(request, f"Supplier or warehouse not found: {supplier_name}, {warehouse_location}")
                    continue

                # Create inventory record
                Inventory.objects.create(
                    product_name=product_name,
                    quantity=int(quantity),
                    price=float(price),
                    supplier=supplier,
                    warehouse=warehouse
                )
                item_added +=1
                

            except Exception as e:
                print(f"error {e}")
        messages.success(request, f"{item_added} Item's  added to inventory.")
        return redirect('inventory')

    return HttpResponse("Invalid request method", status=400)

def billing(request):
    # if request.method == "post":
    if 'auth_token' not in request.session:  
        return redirect('login_user')

    bill = Billing.objects.all()
    return render(request, "billing.html",{"bill":bill})


def add_billing(request):
    if 'auth_token' not in request.session:  
        return redirect('login_user')

    elif request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing')  # Redirect to the billing list page after saving
    else:
        form = BillingForm()
    return render(request, 'add_billing.html', {'form': form})


def sales(request):
    # if request.method == "post":
    if 'auth_token' not in request.session:  
        return redirect('login_user')
    elif request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product # Accessing Inventory instance

            if sale.quantity_sold > product.quantity:
                messages.error(request, f"Not enough stock available. Only {product.quantity} items left.")
                return redirect('sales')
            
            # Calculate the total amount
            sale.total_amount = product.price * sale.quantity_sold
            
            # Update the inventory quantity
            product.quantity -= sale.quantity_sold
            product.save()
            
            # Save the sale
            sale.save()
            
            messages.success(request, "Sale recorded successfully!")
            return redirect('sales')
              # Redirect to the sales list page after saving
    else:
        form = SalesForm()

    sales = Sales.objects.all().order_by('-sale_date')
    tab = request.GET.get('tab', 'sales')
    paginator = Paginator(sales, 5) #Show 5 data 
    page_number = request.GET.get('page') # Get page number from URL
    page_sales = paginator.get_page(page_number) # Get sales for that page

    labels = [sale.sale_date.strftime("%Y-%m-%d") for sale in sales]
    sales_amounts = [sale.total_amount for sale in sales]
    
    
    context = {
        "sales": sales,
        "form":form,
        "tab": tab,
        "labels": labels,
        "sales_amounts": sales_amounts,
        "sales":page_sales,
    } 
    return render(request, "sales.html", context)

from django.db.models import Sum
from .models import Sales, Billing
from django.utils import timezone

def sales_graph(request):
    # Example: Get total sales for the last 30 days
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    sales_data = Sales.objects.filter(sale_date__gte=thirty_days_ago).values('sale_date').annotate(total_sales=Sum('total_amount'))

    # Format data for Chart.js
    labels = [sale['sale_date'].strftime('%Y-%m-%d') for sale in sales_data]
    sales_amounts = [float(sale['total_sales']) for sale in sales_data]

    context = {
        'labels': labels,
        'sales_amounts': sales_amounts,
    }
    return render(request, 'sales_graph.html', context)

def billing_graph(request):
    # Example: Get revenue by payment method
    revenue_by_payment_method = Billing.objects.values('payment_method').annotate(total_revenue=Sum('amount'))

    # Format data for Chart.js
    payment_methods = [item['payment_method'] for item in revenue_by_payment_method]
    revenues = [float(item['total_revenue']) for item in revenue_by_payment_method]

    context = {
        'payment_methods': payment_methods,
        'revenues': revenues,
    }
    return render(request, 'billing_graph.html', context)

def audit_logs(request):
    if not request.user.is_authenticated or request.session.get('user_role') != "Admin":
        messages.error(request, "You don't have permission to view audit logs.")
        return redirect('login_user')
    
    logs = AuditLog.objects.all().order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(logs, 25)  # Show 25 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'audit_logs.html', {'page_obj': page_obj})
