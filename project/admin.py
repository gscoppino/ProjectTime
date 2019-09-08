import datetime
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from .models import Project, Task, Charge


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
            response.context_data['app_list'], 'project', 'Charges', ChargeAdmin.get_default_changelist_url())
        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'], 'project', 'Tasks', TaskAdmin.get_default_changelist_url())

        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super().app_index(request, app_label, extra_context)

        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'], 'project', 'Charges', ChargeAdmin.get_default_changelist_url())
        ProjectTimeAdminSite.update_admin_url(
            response.context_data['app_list'], 'project', 'Tasks', TaskAdmin.get_default_changelist_url())

        return response


admin_site = ProjectTimeAdminSite()


@admin.register(Charge, site=admin_site)
class ChargeAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ('project', 'start_time', 'end_time', 'time_charged',)
    list_filter = ('project', 'start_time',)
    change_list_template = 'charge_change_list.html'

    @staticmethod
    def get_default_changelist_url():
        today = timezone.localtime(timezone.now()).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)

        tomorrow = today + datetime.timedelta(days=1)

        return reverse('admin:project_charge_changelist') + '?' + urlencode({
            'start_time__gte': today,
            'start_time__lt': tomorrow
        })

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_time_charged()

    def time_charged(self, obj):
        return obj.db__time_charged

    time_charged.admin_order_field = 'db__time_charged'


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_charge', 'open_tasks',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_open_task_count().annotate_latest_charge()

    def latest_charge(self, obj):
        if not obj.db__latest_charge:
            return None

        return timezone.localtime(obj.db__latest_charge).date()

    def open_tasks(self, obj):
        return obj.db__open_task_count

    latest_charge.admin_order_field = 'db__latest_charge'
    open_tasks.admin_order_field = 'db__open_task_count'


@admin.register(Task, site=admin_site)
class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'deadline'
    list_display = ('project', 'deadline', 'title', 'done',)
    list_editable = ('deadline', 'title', 'done',)
    list_filter = ('project', 'deadline', 'done',)

    @staticmethod
    def get_default_changelist_url():
        today = timezone.localtime(timezone.now()).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)

        tomorrow = today + datetime.timedelta(days=1)

        return reverse('admin:project_task_changelist') + '?' + urlencode({
            'deadline__gte': today,
            'deadline__lt': tomorrow
        })
