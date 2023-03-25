from django.contrib.admin import register
from atlas.libs.admin import (admin_site, ModelAdminGroup, ADMIN_USER)
from atlas.apps.response.models import (Response, Jawaban)


@register(Response, site=admin_site)
class ResponseAdmin(ModelAdminGroup):
    admin_groups = (ADMIN_USER,)


@register(Jawaban, site=admin_site)
class JawabanAdmin(ModelAdminGroup):
    admin_groups = (ADMIN_USER,)

