""" Defines and instantiates the Admin site for this app
"""

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse_lazy
from django.utils import timezone

from ProjectTime.timezone.views import TimezoneView
from ProjectTime.project.utils import reporting as report_helpers

from ProjectTime.project.models import Project


class ProjectTimeAdminSite(admin.AdminSite):
    """ An Admin site for the project Django app
    """
    site_title = 'ProjectTime'
    site_header = 'ProjectTime'
    index_title = 'ProjectTime Administration'

    def each_context(self, request):
        context = super().each_context(request)

        if context.get('timezone') is not None:
            raise ValueError('Timezone context key would conflict with an '
                             'existing key in the Django admin context.')

        context['timezone'] = request.session.get('timezone') or 'N/A'

        return context

    def get_urls(self):
        urls = super().get_urls()

        extra_urls = [
            path('timezone',
                 self.admin_view(TimezoneView.as_view(
                     success_url=reverse_lazy('admin:index')
                 )),
                 name='select-timezone'),
            path('dashboard',
                 self.admin_view(self.dashboard_view),
                 name='dashboard')
        ]

        return extra_urls + urls

    def dashboard_view(self, request):
        project_ids = request.GET.getlist('project')

        projects = ([
            {
                **project,
                'selected': not project_ids or str(project['id']) in project_ids
            }
            for project in Project.objects.values('id', 'name').order_by('name')
        ])

        series = report_helpers.get_monthly_summary_series(timezone.localtime(), project_ids)
        script, div = report_helpers.get_monthly_summary_chart_components(series)

        context = {
            **self.each_context(request),
            'projects': projects,
            'chart_script': script,
            'chart_div': div
        }

        return TemplateResponse(
            request=request,
            template="admin/dashboard.html",
            context=context
        )


admin_site = ProjectTimeAdminSite()
