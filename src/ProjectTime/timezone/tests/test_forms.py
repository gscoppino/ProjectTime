from django.test import SimpleTestCase
from pytz import common_timezones

from ProjectTime.timezone.forms import TimezoneForm

# Create your tests here.


class TimezoneFormTestCase(SimpleTestCase):
    def test_timezone_field_label(self):
        form = TimezoneForm()
        timezone_field = (form.fields['timezone']
                          .get_bound_field(form, 'timezone'))

        self.assertEqual(timezone_field.label, 'Timezone')

    def test_timezone_field_choices_are_common_timezones(self):
        form = TimezoneForm()
        self.assertEqual(form.fields['timezone'].choices, [
            (tz, tz) for tz in common_timezones
        ])

    def test_timezone_field_initial_value(self):
        form = TimezoneForm()
        self.assertEqual(form.fields['timezone'].initial, 'America/New_York')
