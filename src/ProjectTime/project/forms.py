from django.forms import ModelForm
from ProjectTime.project.models import Charge
from ProjectTime.project.fields import HTML5SplitDateTimeField


class ChargeModelForm(ModelForm):
    class Meta:
        model = Charge
        fields = ('project', 'start_time', 'end_time', 'closed',)
        field_classes = {
            'start_time': HTML5SplitDateTimeField,
            'end_time': HTML5SplitDateTimeField
        }
