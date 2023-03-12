from django.contrib.admin import register
from atlas.libs.admin import (admin_site, ModelAdminGroup, ADMIN_USER)
from atlas.apps.survei.models import (Survei, Pertanyaan, OpsiJawaban)


@register(Survei, site=admin_site)
class SurveiAdmin(ModelAdminGroup):
    admin_groups = (ADMIN_USER,)


@register(Pertanyaan, site=admin_site)
class PertanyaanAdmin(ModelAdminGroup):
    admin_groups = (ADMIN_USER,)


@register(OpsiJawaban, site=admin_site)
class OpsiJawabanAdmin(ModelAdminGroup):
    admin_groups = (ADMIN_USER,)
