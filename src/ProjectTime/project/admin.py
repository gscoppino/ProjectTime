""" Registers custom ModelAdmin's for Django models in this app.
"""

from django.contrib import admin
from django.utils import timezone

from .models import Charge, Project
from .site import admin_site
from .utils.decorators import with_attrs


@admin.register(Charge, site=admin_site)
class ChargeAdmin(admin.ModelAdmin):
    """ A ModelAdmin for charges. At the bottom of the list display, the total
        of the hours on display is shown.
    """
    date_hierarchy = 'start_time'
    list_display = ('project', 'start_time', 'end_time',
                    'time_charged', 'closed',)
    list_editable = ('closed',)
    list_filter = ('project', 'start_time', 'closed',)
    ordering = ('start_time',)
    change_list_template = 'admin/charge/change_list.html'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_time_charged()

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        if obj.closed and not obj.project.active:
            return ('start_time', 'end_time',)
        if obj.closed:
            return ('start_time', 'end_time', 'project',)
        if not obj.project.active:
            return ('start_time', 'end_time', 'closed',)

        return ()

    @with_attrs(admin_order_field='db__time_charged')
    def time_charged(self, obj):
        return obj.db__time_charged


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    """ A ModelAdmin for projects. The latest charge made on each project is
        displayed alongside the project information.
    """
    list_display = ('name', 'latest_charge', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    ordering = ('name',)

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
