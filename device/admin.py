from django.contrib import admin
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import device, oem, model
from .resources import DeviceResource, DeviceExportResource
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.translation import ugettext_lazy as _

class AssigneeListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ASSIGNEE')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'assignee'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('Assigned Devices')),
            ('no', _('Available Devices')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == 'yes':
            return queryset.filter(assignee__isnull=False)
        if self.value() == 'no':
            return queryset.filter(assignee__isnull=True)

class DeviceAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("oem","model","imei","hardware_type","wfi_mac","iccid","mdn","purpose","comment","assignee","assigned_date","return_date")
    list_per_page = 7
    resource_class = DeviceResource
    list_filter = ("oem","model","hardware_type",AssigneeListFilter,)
    search_fields = ["imei","wfi_mac","assignee"]

    def get_export_resource_class(self):
        """
        Returns ResourceClass to use for export.
        """
        return DeviceExportResource

    def get_export_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
        )

        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
        )

        return [f for f in formats if f().can_export()]

admin.site.register(device, DeviceAdmin)
admin.site.register(oem)

class ModelAdmin(admin.ModelAdmin):
    list_display = ("name")
    list_per_page = 7

admin.site.register(model)

# auth.UserAdmin
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ()
    list_filter = ()
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'groups',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ()
    list_filter = ()
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

class CustomGroupAdmin(GroupAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            qs = qs.exclude(codename__in=(
                'add_permission',
                'change_permission',
                'delete_permission',

                'add_contenttype',
                'change_contenttype',
                'delete_contenttype',

                'add_session',
                'delete_session',
                'change_session',

                'add_logentry',
                'change_logentry',
                'delete_logentry',
            ))
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super(GroupAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)