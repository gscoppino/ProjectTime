from django.urls import reverse_lazy
from django.utils.http import urlencode


def get_changelist_url(app_label, model_name, filters):
    return '{path}?{query}'.format(
        path=reverse_lazy('admin:%s_%s_changelist' % (app_label, model_name)),
        query=urlencode(filters))
