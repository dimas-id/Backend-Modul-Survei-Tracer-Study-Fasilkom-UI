from django.contrib.auth.models import (Group, Permission)

from atlas.common.admin import (admin_site, ModelAdminSuperuser)

admin_site.register(Group, admin_class=ModelAdminSuperuser)
admin_site.register(Permission, admin_class=ModelAdminSuperuser)