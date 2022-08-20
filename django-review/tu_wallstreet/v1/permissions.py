from rest_framework.permissions import BasePermission

class GetNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            if request.user.is_authenticated:
                return True
            else:
                return False