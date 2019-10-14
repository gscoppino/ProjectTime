from calendar import monthrange
from datetime import timedelta
from django.contrib import admin
from django.db.models import F, Sum
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.urls import path
from .constants import DEFAULT_PROJECT_CHANGELIST_FILTERS, DEFAULT_CHARGE_CHANGELIST_FILTERS
from .mixins import AdminSiteDefaultFilterMixin
from .models import Project, Charge


class ProjectTimeAdminSite(AdminSiteDefaultFilterMixin, admin.AdminSite):
    site_title = 'ProjectTime'
    site_header = 'ProjectTime'
    index_title = 'ProjectTime Administration'
    default_filters = {
        'project.Project': DEFAULT_PROJECT_CHANGELIST_FILTERS,
        'project.Charge': DEFAULT_CHARGE_CHANGELIST_FILTERS
    }

    def each_context(self, request):
        context = super().each_context(request)

        if context.get('timezone') is not None:
            raise ValueError('Timezone context key would conflict with an'
                             'existing key in the Django admin context.')

        context['timezone'] = request.session.get('timezone') or 'N/A'

        return context

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path('dashboard',
                 self.admin_view(self.dashboard_view),
                 name='dashboard'),

            path('monthly-summary', self.admin_view(self.monthly_summary_view))
        ]

        return extra_urls + urls

    def dashboard_view(self, request):
        context = {
            **self.each_context(request),
            'projects': Project.objects.all()
        }

        return TemplateResponse(request,
                                "admin/dashboard.html",
                                context)

    def monthly_summary_view(self, request):
        project_ids = request.GET.getlist('project')

        queryset = Charge.objects.all()
        if project_ids:
            queryset = queryset.filter(project__in=project_ids)

        today = timezone.localtime()
        start_of_month, end_of_month = monthrange(today.year, today.month)
        limit_day = timedelta(days=1, microseconds=-1)

        return JsonResponse(list((queryset
                                  .filter(start_time__range=(
                                      today.replace(day=start_of_month,
                                                    hour=0,
                                                    minute=0,
                                                    second=0,
                                                    microsecond=0),
                                      today.replace(day=end_of_month,
                                                    hour=0,
                                                    minute=0,
                                                    second=0,
                                                    microsecond=0) + limit_day
                                  ))
                                  .select_related('project')
                                  .values('project')
                                  .order_by('project_id')
                                  .annotate(project_name=F('project__name'))
                                  .annotate(total_time_charged=Sum(
                                      F('end_time') - F('start_time')
                                  )))),
                            safe=False)


admin_site = ProjectTimeAdminSite()
