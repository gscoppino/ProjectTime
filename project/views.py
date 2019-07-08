from django.views import generic as views
from django.utils import timezone as django_timezone
from pytz import timezone
from .forms import TimezoneForm

# Create your views here.


class TimezoneView(views.FormView):
    template_name = 'timezone_form.html'
    form_class = TimezoneForm
    success_url = '/admin/'

    def form_valid(self, form):
        django_timezone.activate(timezone(form.cleaned_data['timezone']))
        return super().form_valid(form)
