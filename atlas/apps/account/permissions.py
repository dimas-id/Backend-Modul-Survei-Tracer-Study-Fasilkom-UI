from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

from atlas.apps.account.models import Account

class IsAdminOrStaff(BasePermission):

    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or \
            request.user.is_staff


class IsAccountOwner(BasePermission):

    def has_object_permission(self, request, view, obj: Account):
        return not request.user.is_anonymous() and request.user.id == obj.id