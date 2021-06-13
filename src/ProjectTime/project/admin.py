""" Registers custom ModelAdmin's for Django models in this app.
"""

from django.contrib import admin
from django.utils import timezone

from .models import Charge, Project
from .site import admin_site


@admin.register(Charge, site=admin_site)
class ChargeAdmin(admin.ModelAdmin):
    """ A ModelAdmin for charges.
    """
    date_hierarchy = 'start_time'
    list_display = ('project', 'start_time', 'end_time',
                    'time_spent', 'closed',)
    list_editable = ('closed',)
    list_filter = ('project', 'start_time', 'closed',)
    ordering = ('start_time',)

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

    @admin.display(ordering='db_time_charged')
    def time_spent(self, obj):
        return obj.db_time_charged


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    """ A ModelAdmin for projects. The latest charge made on each project is
        displayed alongside the project information.
    """
    list_display = ('name', 'last_time_increment', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_latest_charge()

    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.active:
            return ()

        return ('name',)

    @admin.display(ordering='db_latest_charge')
    def last_time_increment(self, obj):
        if not obj.db_latest_charge:
            return None

        return timezone.localtime(obj.db_latest_charge).date()
