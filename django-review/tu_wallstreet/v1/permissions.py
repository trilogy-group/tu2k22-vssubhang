from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import Stocks, Sectors

stock_admin_group, created = Group.objects.get_or_create(name="Stock Admin")

content_type = ContentType.objects.get_for_model(Stocks)
stock_permission = Permission.objects.filter(content_type=content_type)

for perm in stock_permission:
    stock_admin_group.permissions.add(perm)

content_type = ContentType.objects.get_for_model(Sectors)
sector_permission = Permission.objects.filter(content_type=content_type)

for perm in sector_permission:
    stock_admin_group.permissions.add(perm)


class GetNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            if request.user.is_authenticated:
                return True
            else:
                return False

class isStockAdminGroup(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user = request.user
        if request.method == 'POST':
            return user.has_perm('v1.add_stocks')
        elif request.method == 'POST':
            return user.has_perm('v1.change_stocks')
        elif request.method == 'DELETE':
            return user.has_perm('v1.delete_stocks')