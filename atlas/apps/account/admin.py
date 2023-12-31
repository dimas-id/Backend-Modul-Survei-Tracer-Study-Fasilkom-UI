from django.contrib.admin import register
from django.contrib.auth.models import (Group, Permission)

from atlas.libs.admin import (admin_site, ModelAdminGroup, ADMIN_USER)
# register model and admin form
from atlas.apps.account.models import (User, UserProfile)

# account
@register(User, site=admin_site)
class UserAdmin(ModelAdminGroup):
    list_display = ('id', 'first_name', 'last_name', 'email', 'username', 'is_active', 'is_verified')
    search_fields = ('first_name', 'last_name', 'email', 'id')
    list_filter = ('is_staff', 'is_superuser', 'is_verified')
    list_editable = ('is_active', 'is_verified')

    # only admin user can access
    admin_groups = (ADMIN_USER,)

# profile
@register(UserProfile, site=admin_site)
class UserProfileAdmin(ModelAdminGroup):
    list_display = ('user', 'gender', 'birthdate', 'residence_city', 'residence_country')

    # only admin user can access
    admin_groups = (ADMIN_USER,)
