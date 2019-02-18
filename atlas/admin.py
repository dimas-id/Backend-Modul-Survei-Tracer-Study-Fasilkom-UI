from django.contrib.admin import AdminSite

import atlas.apps.account.models as account_models
from rest_framework.authtoken.models import Token

class MyAdminSite(AdminSite):
    site_header = "Altas Administration"
    site_title = "Altas site admin"

admin = MyAdminSite(name="admin")

# register model and admin form

## account
admin.register(account_models.Account)
admin.register(Token)

