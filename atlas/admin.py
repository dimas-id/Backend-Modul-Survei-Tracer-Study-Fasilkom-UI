from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, Permission

class MyAdminSite(AdminSite):
    site_header = "Altas Administration"
    site_title = "Altas site admin"

admin_site = MyAdminSite(name="admin")

# register default models
admin_site.register(Group)
admin_site.register(Permission)
