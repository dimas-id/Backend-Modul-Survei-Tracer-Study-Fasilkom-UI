from django.contrib.admin import register
from django.contrib.auth.models import (Group, Permission)

from atlas.common.admin import (admin_site, ModelAdminSuperuser)
# register model and admin form
from atlas.apps.account.models import (User, UserProfile, UserPreference)

# account
@register(User, site=admin_site)
class UserAdmin(ModelAdminSuperuser):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'profile')

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

# profile
@register(UserProfile, site=admin_site)
class UserProfileAdmin(ModelAdminSuperuser):
    list_display = ('user', 'gender', 'birthdate', 'latest_csui_class','residence_city', 'residence_country')

# register default models
admin_site.register(Group, admin_class=ModelAdminSuperuser)
admin_site.register(Permission, admin_class=ModelAdminSuperuser)
admin_site.register(UserPreference)