""" Defines the forms used by views in this app
"""

from django.forms import ModelForm

from ProjectTime.project.fields import HTML5SplitDateTimeField
from ProjectTime.project.models import Charge


class ChargeModelForm(ModelForm):
    class Meta:
        model = Charge
        fields = ('project', 'start_time', 'end_time', 'closed',)
        field_classes = {
            'start_time': HTML5SplitDateTimeField,
            'end_time': HTML5SplitDateTimeField
        }
