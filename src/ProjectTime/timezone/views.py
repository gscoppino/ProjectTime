from django.views import generic as views
from .forms import TimezoneForm

# Create your views here.


class TimezoneView(views.FormView):
    template_name = 'timezone_form.html'
    form_class = TimezoneForm

    def form_valid(self, form):
        self.request.session['timezone'] = form.cleaned_data['timezone']
        return super().form_valid(form)