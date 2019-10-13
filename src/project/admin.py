from django.contrib import admin
from django.utils import timezone
from .constants import DEFAULT_PROJECT_CHANGELIST_FILTERS, DEFAULT_CHARGE_CHANGELIST_FILTERS
from .mixins import ModelAdminDefaultFilterMixin
from .models import Project, Charge
from .site import admin_site
from .utils import with_attrs


@admin.register(Charge, site=admin_site)
class ChargeAdmin(ModelAdminDefaultFilterMixin, admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ('project', 'start_time', 'end_time',
                    'time_charged', 'closed',)
    list_editable = ('closed',)
    list_filter = ('project', 'start_time', 'closed',)
    change_list_template = 'admin/project/charge/change_list.html'
    change_form_template = 'admin/project/charge/change_form.html'
    default_filters = DEFAULT_CHARGE_CHANGELIST_FILTERS

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_time_charged()

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        elif obj.closed and not obj.project.active:
            return ('start_time', 'end_time',)
        elif obj.closed:
            return ('start_time', 'end_time', 'project',)
        elif not obj.project.active:
            return ('start_time', 'end_time', 'closed',)
        else:
            return ()

    @with_attrs(admin_order_field='db__time_charged')
    def time_charged(self, obj):
        return obj.db__time_charged


@admin.register(Project, site=admin_site)
class ProjectAdmin(ModelAdminDefaultFilterMixin, admin.ModelAdmin):
    list_display = ('name', 'latest_charge', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    change_form_template = "admin/project/charge/change_form.html"
    default_filters = DEFAULT_PROJECT_CHANGELIST_FILTERS

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_latest_charge()

    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.active:
            return ()

        return ('name',)

    @with_attrs(admin_order_field='db__latest_charge')
    def latest_charge(self, obj):
        if not obj.db__latest_charge:
            return None

        return timezone.localtime(obj.db__latest_charge).date()
