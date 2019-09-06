from django.contrib import admin
from .models import Project, Task, Charge


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('project', 'date', 'start_time',
                    'end_time', 'time_charged',)
    list_filter = ('project', 'date',)
    change_list_template = 'charge_change_list.html'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_time_charged()

    def time_charged(self, obj):
        return obj.db__time_charged

    time_charged.admin_order_field = 'db__time_charged'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_charge', 'open_tasks',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_open_task_count().annotate_latest_charge()

    def latest_charge(self, obj):
        return obj.db__latest_charge

    def open_tasks(self, obj):
        return obj.db__open_task_count

    latest_charge.admin_order_field = 'db__latest_charge'
    open_tasks.admin_order_field = 'db__open_task_count'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('project', 'date', 'title', 'done',)
    list_editable = ('date', 'title', 'done',)
    list_filter = ('project', 'date', 'done',)
