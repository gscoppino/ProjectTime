""" Defines the routable views for this app
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from ProjectTime.project.filters import ChargeFilter, ProjectFilter
from ProjectTime.project.forms import ChargeModelForm
from ProjectTime.project.models import Charge, Project
from ProjectTime.project.tables import ChargeTable, ProjectTable
from ProjectTime.project.utils import reporting as report_helpers
from ProjectTime.timezone.forms import TimezoneForm


class IndexView(LoginView):
    template_name = "project/login_form.html"
    redirect_authenticated_user = True


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "project/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_projects = (Project.objects
                           .filter(active=True)
                           .order_by('name')
                           .annotate_latest_charge()
                           )

        open_charges = (Charge.objects
                        .filter(closed=False)
                        .select_related('project')
                        .order_by('start_time')
                        .annotate_time_charged()
                        )

        month_summary_chart_height = 600
        month_summary_chart_script, month_summary_chart_div = (
            report_helpers.get_monthly_summary_chart_components(
                report_helpers.get_monthly_summary_series(
                    timezone.localtime()
                ),
                sizing_mode="stretch_width",
                height=month_summary_chart_height,
            )
        )

        has_timezone = self.request.session.get('timezone')

        context['active_projects'] = active_projects
        context['open_charges'] = open_charges
        context['month_summary_chart_script'] = month_summary_chart_script
        context['month_summary_chart_div'] = month_summary_chart_div
        context['month_summary_chart_height'] = month_summary_chart_height
        context['timezone_form'] = TimezoneForm() if not has_timezone else None

        return context


class ProjectListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Project
    table_class = ProjectTable
    table_pagination = {'per_page': 10}
    filterset_class = ProjectFilter

    def get_queryset(self):
        return super().get_queryset().annotate_latest_charge()

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs.update({'order_by': 'name'})
        return kwargs


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('name', 'active',)
    success_url = reverse_lazy('project:project-list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ('name', 'active',)
    success_url = reverse_lazy('project:project-list')


class ChargeListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Charge
    table_class = ChargeTable
    table_pagination = {'per_page': 10}
    filterset_class = ChargeFilter

    def get_queryset(self):
        return super().get_queryset().select_related('project').annotate_time_charged()

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs.update({'order_by': 'start_time'})
        return kwargs


class ChargeCreateView(LoginRequiredMixin, CreateView):
    model = Charge
    form_class = ChargeModelForm
    success_url = reverse_lazy('project:charge-list')

    def get_initial(self):
        initial = super().get_initial()

        now = timezone.localtime()
        initial['start_time'] = now

        return initial


class ChargeUpdateView(LoginRequiredMixin, UpdateView):
    model = Charge
    form_class = ChargeModelForm
    success_url = reverse_lazy('project:charge-list')


class ChargeCloseView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, _, pk):
        charge = Charge.objects.get(pk=pk)
        charge.closed = True
        charge.validate_and_save()
        return HttpResponseRedirect(reverse('dashboard'))
