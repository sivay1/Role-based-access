from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == 'Admin'

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == 'Manager'

class IsFranchiseOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == 'Franchise Owner'

class IsLogisticsPersonnel(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == 'Logistics Personnel'

class IsCustomerSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role.name == 'Customer Support'