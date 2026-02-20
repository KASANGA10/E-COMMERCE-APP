from rest_framework import permissions

class IsShopManager(permissions.BasePermission):
    """
    Allows access only to managers of the specific shop.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user has a manager profile linked to the shop of the product
        try:
            return request.user.manager_profile.shop == obj.shop
        except AttributeError:
            return False