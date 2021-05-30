from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from ProjectTime.project.forms import ChargeModelForm
from ProjectTime.project.models import Project, Charge
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


class ProjectListView(ListView):
    model = Project
    paginate_by = 10

    def get_queryset(self):
        return (super()
                .get_queryset()
                .order_by('name')
                .annotate_latest_charge()
                )


class ProjectCreateView(CreateView):
    model = Project
    fields = ('name', 'active',)
    success_url = reverse_lazy('dashboard')


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('name', 'active',)
    success_url = reverse_lazy('dashboard')


class ChargeListView(ListView):
    model = Charge
    ordering = 'start_time'
    paginate_by = 10

    def get_queryset(self):
        return (super()
                .get_queryset()
                .select_related('project')
                .annotate_time_charged()
                )


class ChargeCreateView(CreateView):
    model = Charge
    form_class = ChargeModelForm
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super().get_initial()

        now = timezone.localtime()
        initial['start_time'] = now

        return initial


class ChargeUpdateView(UpdateView):
    model = Charge
    form_class = ChargeModelForm
    success_url = reverse_lazy('dashboard')


class ChargeCloseView(View):
    http_method_names = ['post']

    def post(self, _, pk):
        charge = Charge.objects.get(pk=pk)
        charge.closed = True
        charge.full_clean()
        charge.save()
        return HttpResponseRedirect(reverse('dashboard'))
