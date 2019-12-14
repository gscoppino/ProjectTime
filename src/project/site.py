import pandas as pd
from calendar import monthrange
from datetime import timedelta
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from django.contrib import admin
from django.db.models import F, Sum
from django.template.response import TemplateResponse
from django.utils import timezone
from django.urls import path, reverse_lazy
from math import pi
from timezone.views import TimezoneView
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

    def get_monthly_summary_series(self, date, project_ids=[]):
        charges = Charge.objects.all()
        if project_ids:
            charges = charges.filter(project__in=project_ids)

        _, end_of_month = monthrange(date.year, date.month)
        limit_day = timedelta(days=1, microseconds=-1)

        charges = (charges
                   .filter(start_time__range=(
                       date.replace(day=1,
                                    hour=0,
                                    minute=0,
                                    second=0,
                                    microsecond=0),
                       date.replace(day=end_of_month,
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
                   )))

        chart_data = ({
            charge['project_name']:
            charge['total_time_charged'].total_seconds() / 3600
            for charge in charges
        })

        series = (pd.Series(chart_data)
                  .reset_index(name='value')
                  .rename(columns={'index': 'charge'}))

        series['angle'] = series['value'] / series['value'].sum() * (2 * pi)

        category_count = len(chart_data)
        if category_count <= 20:
            series['color'] = (Category20c[len(chart_data)]
                               if category_count >= 3
                               else Category20c[3][0:category_count])

        return series

    def get_monthly_summary_chart_components(self, series):
        chart = figure(title="Monthly Summary",
                       toolbar_location=None,
                       tools="hover",
                       tooltips="@charge: @value hour(s)",
                       x_range=(-0.5, 1.0))

        chart.wedge(source=series,
                    x=0,
                    y=1,
                    radius=0.4,
                    start_angle=cumsum('angle', include_zero=True),
                    end_angle=cumsum('angle'),
                    line_color='white',
                    fill_color='color',
                    legend_field='charge')

        chart.axis.axis_label = None
        chart.axis.visible = False
        chart.grid.grid_line_color = None

        return components(chart)

    def dashboard_view(self, request):
        project_ids = request.GET.getlist('project')

        projects = ([
            {
                **project,
                'selected': not project_ids or str(project['id']) in project_ids
            }
            for project in Project.objects.values('id', 'name').order_by('name')
        ])

        series = self.get_monthly_summary_series(
            timezone.localtime(),
            project_ids)

        script, div = self.get_monthly_summary_chart_components(series)

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
