from rest_framework import serializers
from django.contrib.auth.models import User
from franchise.models import *
from django.contrib.auth.models import User
from .models import Role, Profile
# from .models import Shipment, Order
# from .models import Inventory, Supplier
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Profile, Role


class RegisterSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(write_only=True)  # Accept role during registration

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # role_name = validated_data.pop('role', 'CustomerSupport')  # Default role
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        role = Role.objects.get(name="Customer Support")
        Profile.objects.create(user=user, role=role)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(write_only=True)  # Add role field

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # role_name = validated_data.pop('role', 'CustomerSupport')  # Default role
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        role = Role.objects.get(name="Customer Support")  # Use role.name
        Profile.objects.create(user=user, role=role)  # Assign role to user
        Token.objects.create(user=user)  # Create a token for the new user
        return user
