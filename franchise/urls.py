from django.urls import path
from . import views
from franchise.views import (
    RegisterAPIView,LoginAPIView,register_user,login
)
urlpatterns = [
    # path('', views.login, name="home"),
    # path('users/',views.user_list, name = "users"),
    # path("reports/", views.reports, name = "reports"),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('register_user/', views.register_user, name='register_user'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('login_user/', views.login, name='login_user'),
    path("logout/", views.logoutUser, name = "logout"),   

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),
    
    path('manage-users/', views.manage_users, name='manage_users'),
    path('update-role/<int:user_id>/', views.update_role, name='update_role'),
]