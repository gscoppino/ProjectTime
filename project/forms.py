from django import forms
from pytz import common_timezones


class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in common_timezones], initial='America/New_York')
