from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.views.generic import FormView
from django.views.generic.edit import FormMixin

from ProjectTime.timezone.forms import TimezoneForm
from ProjectTime.timezone.views import TimezoneView


class ViewTestCase(TestCase):
    def setup_class_based_view(self, view_class, request, *args, **kwargs):
        """
        Mimic ``as_view()``, but returns view instance.
        Use this function to get view instances on which you can run unit tests,
        by testing specific methods.
        """
        view = view_class()
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view


class TimezoneViewTestCase(ViewTestCase):
    def test_inherits_from_django_formview(self):
        self.assertTrue(issubclass(TimezoneView, FormView))

    def test_timezone_form_template_is_used(self):
        self.assertTrue(TimezoneView.template_name == 'timezone_form.html')

    def test_timezone_form_is_used(self):
        self.assertTrue(TimezoneView.form_class is TimezoneForm)

    def test_set_timezone_for_session_on_successful_submit(self):
        request = RequestFactory().get('/foo/bar')
        request.session = {}

        view = self.setup_class_based_view(TimezoneView, request)

        form = TimezoneForm(data={
            'timezone': 'America/New_York'
        })

        form.full_clean()

        with patch.object(FormMixin, 'form_valid'):
            view.form_valid(form)

        self.assertEqual(request.session['timezone'], 'America/New_York')
