""" Defines the fields used by forms in this app
"""

from django.forms import SplitDateTimeField
from ProjectTime.project.widgets import HTML5SplitDateTimeWidget


class HTML5SplitDateTimeField(SplitDateTimeField):
    """ SplitDateTimeField, with a custom default widget that uses HTML5 input types
        for date and time instead of the default text input type.
    """

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = HTML5SplitDateTimeWidget
        super().__init__(*args, **kwargs)
