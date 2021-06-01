""" Defines the widgets used by fields in this app
"""

from django.forms import SplitDateTimeWidget


class HTML5SplitDateTimeWidget(SplitDateTimeWidget):
    """ SplitDateTimeWidget, but with the date and time subwidgets rendered as
        HTML5 date and time types, respectively, instead of the default text type.
    """

    def __init__(self, *args, **kwargs):
        date_attrs = kwargs.pop("date_attrs", {})
        date_attrs.update({'type': 'date'})
        kwargs["date_attrs"] = date_attrs

        time_attrs = kwargs.pop("time_attrs", {})
        time_attrs.update({'type': 'time'})
        kwargs["time_attrs"] = time_attrs

        super().__init__(*args, **kwargs)
