from django.contrib.admin import ModelAdmin
from django.contrib.admin import AdminSite

# specific admin
# admin only is superuser
# this specific admin is staff and based on grouping
ADMIN_CHANNEL = 'admin_channel'
ADMIN_DONATION = 'admin_donation'
ADMIN_USER = 'admin_user'
MANAGEMENT = 'management'


class ModelAdminGroup(ModelAdmin):
    """
    https://docs.djangoproject.com/en/2.2/ref/contrib/admin/

    # Custom
    autocomplete_fields = ()
    readonly_fields = ()
    fields = None
    exclude = None
    form = forms.ModelForm
    ordering = None
    sortable_by = None

    list_display = ('__str__',)
    list_display_links = ()
    list_filter = ()
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ()
    search_fields = ()
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    paginator = Paginator
    preserve_filters = True
    inlines = []

    # Custom templates (designed to be over-ridden in subclasses)
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

    # Actions
    actions = []
    action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    """

    # backward compability so everyone still can access all
    # and step by step remove it by using inheritance
    admin_groups = [ADMIN_CHANNEL, ADMIN_DONATION, ADMIN_USER, MANAGEMENT]

    def get_admin_groups(self):
        return self.admin_groups

    def is_member(self, user):
        """
        Check if a user is member of a group
        """
        if not user.is_staff:
            return False

        user_groups = getattr(user, 'groups', []).all().values('name')
        for g in user_groups:
            if g.get('name') in self.get_admin_groups():
                return True
        return False

    def has_view_or_change_permission(self, request, obj=None):
        """
        You can override this method based on your need
        """
        return self.has_view_permission(request, obj) or self.has_change_permission(request, obj)

    def has_add_permission(self, request):
        """
        You can override this method based on your need
        """
        return request.user.is_superuser or self.is_member(request.user)

    def has_module_permission(self, request):
        """
        You can override this method based on your need
        """
        return request.user.is_superuser or self.is_member(request.user)

    def has_change_permission(self, request, obj=None):
        """
        You can override this method based on your need
        """
        return request.user.is_superuser or self.is_member(request.user)

    def has_view_permission(self, request, obj=None):
        """
        You can override this method based on your need
        """
        return request.user.is_superuser or self.is_member(request.user)

    def has_delete_permission(self, request, obj=None):
        """
        You can override this method based on your need
        """
        return False


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
