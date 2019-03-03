from django.conf import settings

from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

from atlas.apps.account.models import User


class IsAnonymous(BasePermission):
    """Only allow unauthenticated user"""

    def has_permission(self, request, view):
        return request.user.is_anonymous


class AllowedRegister(BasePermission):
    message = 'Register feature are temporarily disabled.'

    def has_permission(self, request, view):
        return settings.ALLOW_NATIVE_REGISTER


class VerifiedAccount(BasePermission):
    message = 'Please verify your email and/or complete your profile first.'

    def has_permission(self, request, view):
        return request.user.is_verified


class CompleteProfile(BasePermission):
    message = 'Please complete your profile first.'

    def has_permission(self, request, view):
        return request.user.is_completed


class IsAdminOrStaff(BasePermission):

    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or \
            request.user.is_staff


class IsUserOwner(BasePermission):

    def has_object_permission(self, request, view, obj: User):
        return not request.user.is_anonymous and request.user.id == obj.id
