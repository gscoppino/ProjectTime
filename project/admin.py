from django.contrib import admin
from .models import Project, Charge


class ChargeInline(admin.TabularInline):
    model = Charge
    extra = 1

    def get_queryset(self, request):
        return Charge.objects.none()


class ChargeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('project', 'date', 'start_time',
                    'end_time', 'time_charged',)
    list_editable = ('date', 'start_time', 'end_time',)
    list_filter = ('project', 'date',)
    change_list_template = 'charge_change_list.html'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_time_charged()

    def time_charged(self, obj):
        return obj.db__time_charged


class ProjectAdmin(admin.ModelAdmin):
    inlines = (ChargeInline,)


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Charge, ChargeAdmin)
