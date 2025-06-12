from rest_framework.permissions import BasePermission

class IsUserSuperuser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return True if (request.user and request.user.is_authenticated and request.user.is_superuser) else False
    
class IsRestaurantAdmin(BasePermission):
    """
    Allows access only to the admin of the restaurant.
    """

    def has_permission(self, request, view):
        return True if (request.user.role == "franchise_owner") else False
    
    def has_object_permission(self, request, view, obj):
        
        if not obj:
            return False

        return True if obj.admin == request.user or request.user.is_superuser else False
    
class IsOutletOrFranchiseAdmin(BasePermission):
    """
    Allows access only to the admin of the outlet or the admin of the franchise the outlet belongs to.
    """
    
    def has_permission(self, request, view):                        
        return True if request.user.role in ["franchise_owner", "outlet_owner"] else False
    
    def has_object_permission(self, request, view, obj):        
        # For MenuCategory, MenuItem, Order, OrderItem, get the outlet        
        if not obj:
            return False

        return (obj.admin == request.user) or (obj.franchise.admin == request.user)
    
class IsOutletAdmin(BasePermission):
    """
    Allows access only to the admin of the outlet.
    """
    
    def has_permission(self, request, view):        
        return True if request.user.role == "outlet_owner" else False    