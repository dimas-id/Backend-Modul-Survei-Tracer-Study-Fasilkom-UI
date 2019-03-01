from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

from atlas.apps.account.models import User

class IsAdminOrStaff(BasePermission):

    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or \
            request.user.is_staff


class IsUserOwner(BasePermission):

    def has_object_permission(self, request, view, obj: User):
        return not request.user.is_anonymous() and request.user.id == obj.id