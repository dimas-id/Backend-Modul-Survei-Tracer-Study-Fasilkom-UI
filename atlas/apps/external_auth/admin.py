from atlas.libs.admin import admin_site
from atlas.apps.external_auth import models

# Register your models here.
admin_site.register(models.LinkedinAccount)