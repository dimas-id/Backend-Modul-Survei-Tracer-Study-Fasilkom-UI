from django.contrib.admin import ModelAdmin, register
from atlas.admin import admin_site

# register model and admin form
from atlas.apps.account.models import User

# account
@register(User, site=admin_site)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')

    def has_view_or_change_permission(self, request, obj=None):
        return super().has_view_or_change_permission(request, obj=obj) \
            and request.user.is_superuser

    def has_add_permission(self, request):
        return super().has_add_permission(request) \
            and request.user.is_superuser

    def has_module_permission(self, request):
        return super().has_module_permission(request) \
            and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj=obj) \
            and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False
