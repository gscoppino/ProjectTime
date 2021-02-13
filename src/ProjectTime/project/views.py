from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView

from ProjectTime.project.models import Project, Charge
from ProjectTime.project.utils import reporting as report_helpers

@staff_member_required
def home(request):
    return HttpResponseRedirect(reverse('admin:index'))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "project/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_projects = (Project.objects
            .filter(active=True)
            .annotate_latest_charge()
        )

        open_charges = (Charge.objects
            .filter(closed=False)
            .select_related('project')
            .annotate_time_charged()
        )

        month_summary_chart_script, month_summary_chart_div = (
            report_helpers.get_monthly_summary_chart_components(
                report_helpers.get_monthly_summary_series(timezone.localtime())
            )
        )


        context['active_projects'] = active_projects
        context['open_charges'] = open_charges
        context['month_summary_chart_script'] = month_summary_chart_script
        context['month_summary_chart_div'] = month_summary_chart_div

        return context
