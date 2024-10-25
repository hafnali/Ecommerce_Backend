
from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','Post']:
            return True
        return request.user and request.user.is_staff





