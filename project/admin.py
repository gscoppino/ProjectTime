from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from .models import Project, Charge
from .utils import with_attrs


class ProjectTimeAdminSite(admin.AdminSite):
    site_title = 'ProjectTime'
    site_header = 'ProjectTime'
    index_title = 'ProjectTime Administration'

    @staticmethod
    def update_admin_url(app_list, app_label, model_name, url):
        for app in app_list:
            if app['app_label'] == app_label:
                for model in app['models']:
                    if model['name'] == model_name:
                        model['admin_url'] = url
                        break

    def index(self, request, extra_context=None):
        response = super().index(request, extra_context)

        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'],
            'project',
            'Projects',
            ProjectAdmin.get_default_changelist_url())

        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'],
            'project',
            'Charges',
            ChargeAdmin.get_default_changelist_url())

        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super().app_index(request, app_label, extra_context)

        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'],
            'project',
            'Projects',
            ProjectAdmin.get_default_changelist_url())

        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'],
            'project',
            'Charges',
            ChargeAdmin.get_default_changelist_url())

        return response


admin_site = ProjectTimeAdminSite()


@admin.register(Charge, site=admin_site)
class ChargeAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ('project', 'start_time', 'end_time',
                    'time_charged', 'closed',)
    list_editable = ('closed',)
    list_filter = ('project', 'start_time', 'closed',)
    change_list_template = 'charge_change_list.html'
    change_form_template = 'charge_change_form.html'

    @staticmethod
    def get_default_changelist_url():
        return '{path}?{query}'.format(
            path=reverse('admin:project_charge_changelist'),
            query=urlencode({'closed__exact': 0})
        )

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
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_charge', 'active',)
    list_editable = ('active',)
    list_filter = ('active',)
    change_form_template = "project_change_form.html"

    @staticmethod
    def get_default_changelist_url():
        return '{path}?{query}'.format(
            path=reverse('admin:project_project_changelist'),
            query=urlencode({'active__exact': 1})
        )

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
