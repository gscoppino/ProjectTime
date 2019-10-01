from django.urls import reverse_lazy
from django.utils.http import urlencode

def with_attrs(**attrs):
    def with_attrs(f):
        for k,v in attrs.items():
            setattr(f, k, v)
        return f

    return with_attrs

def get_changelist_url(app_label, model_name, filters):
    return '{path}?{query}'.format(
        path=reverse_lazy('admin:%s_%s_changelist' % (app_label, model_name)),
        query=urlencode(filters))