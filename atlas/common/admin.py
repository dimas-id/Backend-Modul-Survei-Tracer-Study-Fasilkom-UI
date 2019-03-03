from django.contrib.admin import ModelAdmin
from django.contrib.admin import AdminSite

class ModelAdminSuperuser(ModelAdmin):

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


class MyAdminSite(AdminSite):
    site_header = "Altas Administration"
    site_title = "Altas site admin"

admin_site = MyAdminSite(name="admin")
