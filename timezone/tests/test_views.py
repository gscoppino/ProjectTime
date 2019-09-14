from django.shortcuts import reverse
from django.test import TestCase
from timezone.forms import TimezoneForm

# Create your tests here.


class TimezoneViewTestCase(TestCase):
    def test_view_is_ok(self):
        response = self.client.get(reverse('select-timezone'))
        self.assertEqual(response.status_code, 200)

    def test_timezone_form_template_is_used(self):
        response = self.client.get(reverse('select-timezone'))
        self.assertTemplateUsed(response, 'timezone_form.html')

    def test_timezone_form_is_used(self):
        response = self.client.get(reverse('select-timezone'))
        self.assertIsInstance(response.context['form'], TimezoneForm)

    def test_set_timezone_for_session_on_successful_submit(self):
        self.assertEqual('timezone' in self.client.session, False)

        self.client.post(reverse('select-timezone'), {
            'timezone': 'America/New_York'
        })

        self.assertEqual(self.client.session['timezone'], 'America/New_York')

    def test_redirects_to_login_on_successful_submit(self):
        response = self.client.post(reverse('select-timezone'), {
            'timezone': 'America/New_York'
        })

        self.assertRedirects(
            response,
            reverse('admin:index'),
            fetch_redirect_response=False)
