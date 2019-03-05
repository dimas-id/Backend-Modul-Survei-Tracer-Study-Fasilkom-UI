# from django.contrib.admin import register

from atlas.common.admin import (admin_site, ModelAdminSuperuser)
from atlas.apps.experience.models import Position, Education


admin_site.register(Position, site=admin_site)
admin_site.register(Education, site=admin_site)
