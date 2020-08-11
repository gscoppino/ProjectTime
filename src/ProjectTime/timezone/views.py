""" Defines the Django views for this app
"""

from django.views import generic as views

from .forms import TimezoneForm


class TimezoneView(views.FormView):  # pylint: disable=too-many-ancestors
    """ View to set the timezone for a user session
    """
    template_name = 'timezone_form.html'
    form_class = TimezoneForm

    def form_valid(self, form):
        self.request.session['timezone'] = form.cleaned_data['timezone']
        return super().form_valid(form)
