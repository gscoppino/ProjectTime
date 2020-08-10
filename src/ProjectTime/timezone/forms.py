""" Django forms for the timezone Django app.
"""

from django import forms
from pytz import common_timezones


class TimezoneForm(forms.Form):
    """ Form to set the timezone for a user session.
    """
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in common_timezones],
        initial='America/New_York')
