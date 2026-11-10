from rest_framework import permissions

class IsSuperUserOrAdminOrReadOnly(permissions.BasePermission):
    """Controle de acessos"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if hasattr(view, 'queryset') and view.queryset.model.__name__ == 'User':
            return request.user.is_superuser

        return request.user.is_staff or request.user.is_superuser