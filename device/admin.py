from django.contrib import admin
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import device, oem, model
from .models import device, oem, model
from .resources import DeviceResource
# Register your models here.


class DeviceAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ("imei","oem","model","delivery","wfi_mac","iccid","imsi","mdn","purpose","comment","assignee","assigned_date","return_date")
    list_per_page = 7
    resource_class = DeviceResource
    list_filter = ("oem","model","delivery")
    fields = ("imei","oem","model","delivery","wfi_mac","iccid","imsi","mdn","purpose","comment","assignee","assigned_date","return_date")
    search_fields = ["imei","wfi_mac","assignee"]


    # actions = [export_to_csv]
    # list_display_links = ()
    # list_select_related = ('oem', 'category')
    # list_select_related = False
    # list_per_page = 100
    # list_max_show_all = 200
    # list_editable = ()
    # search_fields = ()
    # date_hierarchy = None
    # save_as = False
    # save_as_continue = True
    # save_on_top = False
    # paginator = Paginator
    # preserve_filters = True
    # inlines = []

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
    # resource_class = DeviceResource
    # actions = [export_to_csv]
    # list_display_links = ()
    # list_filter = ("imei","oem","model")
    # list_select_related = ('oem', 'category')
    # list_select_related = False
    # list_per_page = 100
    # list_max_show_all = 200
    # list_editable = ()
    # search_fields = ()
    # date_hierarchy = None
    # save_as = False
    # save_as_continue = True
    # save_on_top = False
    # paginator = Paginator
    # preserve_filters = True
    # inlines = []
    # fields = ("oem","name")
    # search_fields = ["imei","wfi_mac","iccid","imsi","mdn"]

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


from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.translation import ugettext_lazy as _

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
