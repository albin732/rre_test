from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if hasattr(view, 'permissions_required'):
                return bool(view.permissions_required.get(request.method.upper()) in request.permissions)
            return True
        return False
