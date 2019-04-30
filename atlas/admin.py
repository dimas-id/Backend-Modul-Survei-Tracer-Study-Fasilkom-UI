from django.contrib.auth.models import Group

from atlas.libs.admin import (admin_site, ModelAdminSuperuser)

admin_site.register(Group)