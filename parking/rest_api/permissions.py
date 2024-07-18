from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employee)

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user owns any vehicle associated with the parking detail
        user = request.user
        if hasattr(user, 'vehicle_owner'):
            return obj.vehicles.filter(owner=user.vehicle_owner).exists()
        return False