from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login as auth_login,logout
from .forms import UserForm
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from franchise.models import Profile,Role,Report
from franchise.serializers import UserSerializer,RegisterSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
import requests,json
from django.shortcuts import get_object_or_404
from inventory.models import Inventory
class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            role = user.profile.role.name
            return Response({'token': token.key,'role': role}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
BASE_URL = "http://127.0.0.1:8000"

def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        print(f"Received role: {role}")
        response = requests.post(f'{BASE_URL}/api/login/', data={
            'username': username,
            'password': password,
            'role':role
        })
        if response.status_code == 200:
            
            token = response.json().get('token')
            user_role = response.json().get('role')  
            request.session['auth_token'] = token
            request.session['user_role'] = user_role
            print(f"Role: {user_role}")

            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)  # This sets request.user
                

            if user_role == "Admin":
                return redirect('admin_dashboard')
            elif user_role == "Manager":
                return redirect('manager_dashboard')
            elif user_role == "Franchise Owner":
                return redirect('owner_dashboard')
                     
            
            else:    
                print("Token stored in session:", token)
                return redirect('login_user')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register_user(request):
   if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
        # Prepare data for the API request
            data = {
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password1'),
            }
            
            try:
                response = requests.post(f'{BASE_URL}/api/register/', json=data)
                print("API Response:", response.status_code, response.json())

                if response.status_code == 201:
                    # Redirect to the login page after successful registration
                    messages.info(request,"Registration success please login to continue!.")
                    return redirect('login_user')
                elif response.status_code == 400:
                    # Display errors if registration fails
                    return render(request, 'register.html', {'form': form, 'error': response.json()})
                else:
                    return render(request, 'register.html', {'form': form, 'error': {'error': ['Unexpected error occurred.']}})
            except requests.exceptions.RequestException as e:
                return render(request, 'register.html', {'form': form, 'error': {'error': ['Failed to connect to the API.']}})
        else:
            # Display form errors if validation fails
            print(form.errors)
            return render(request, 'register.html', {'form': form})
    
    # Render the registration form for GET requests
   form = UserForm()
   return render(request, 'register.html',{'form': form})

def admin_dashboard(request):
    
    if 'auth_token' not in request.session:  # Check if user is authenticated
        return redirect('login_user')
    threshold = 10  # Set your low stock threshold
    low_stock_items = Inventory.objects.filter(quantity__lte=threshold).order_by('quantity')
    
    # Prepare chart data
    chart_data = {
        'labels': [item.product_name for item in low_stock_items],
        'quantities': [item.quantity for item in low_stock_items],
        'threshold': threshold,
        'colors': [
            '#e74a3b' if qty < 5 else  # Red for critical stock (below 5)
            '#f6c23e' if qty < 10 else  # Yellow for warning stock
            '#1cc88a'                   # Green (shouldn't appear since we filtered <=10)
            for qty in [item.quantity for item in low_stock_items]
        ]
    }
    
    return render(request, 'admin_dashboard.html', {
        'chart_data': json.dumps(chart_data),
        'low_stock_count': low_stock_items.count()
    })

def manager_dashboard(request):
    if 'auth_token' not in request.session:  # Check if user is authenticated
        return redirect('login_user') 
    return render(request, 'manager_dashboard.html')

def owner_dashboard(request):
    if 'auth_token' not in request.session:  # Check if user is authenticated
        return redirect('login_user') 
    return render(request, 'owner_dashboard.html')

def manage_users(request):
    if request.session.get('user_role') != "Admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login_user')  # Restrict access to Admins only
        

    users = Profile.objects.select_related('user').all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def update_role(request, user_id):
    if request.session.get('user_role') != "Admin":
        return redirect('login_user')  # Restrict non-admins

    if request.method == "POST":
        new_role_name = request.POST.get("role")
        if new_role_name == "Select Role":
            messages.error(request, "Please select a valid role")
            return redirect('manage_users')
        user_profile = get_object_or_404(Profile, user_id=user_id)
        new_role = get_object_or_404(Role, name=new_role_name)
        user_profile.role = new_role
        user_profile.save()
        if user_profile:
            messages.success(request, "Role update success!.")
        
    return redirect('manage_users')

def logoutUser(request):
    logout(request)
    return redirect('login_user')