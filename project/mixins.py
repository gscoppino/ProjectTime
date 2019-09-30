from django.urls import reverse_lazy
from django.utils.http import urlencode


class AdminSiteDefaultFilterMixin:
    """
    A mixin for classes that inherit from django.contrib.admin.AdminSite
    It augments the default changelist URL's with filters defined on the class
    as "default_filters", which should be a dictionary mapping app models
    to a dictionary that maps filter field names to values e.g.
    {'test_app.test_model': {'name__exact': 'name'}}
    """
    @classmethod
    def set_default_changelist_filter(cls, app_list, app_label, model_name, filters):
        for app in app_list:
            if app['app_label'] == app_label:
                for model in app['models']:
                    if model['object_name'] == model_name:
                        model['admin_url'] = '{path}?{query}'.format(
                            path=model['admin_url'],
                            query=urlencode(filters))

                        break

    @classmethod
    def set_default_changelist_filters(cls, app_list):
        for key, filter in cls.default_filters.items():
            app_label, model_name = key.split('.')
            cls.set_default_changelist_filter(app_list,
                                              app_label,
                                              model_name,
                                              filter)

    def index(self, request, extra_context=None):
        response = super().index(request, extra_context)
        self.set_default_changelist_filters(response.context_data['app_list'])
        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super().app_index(request, app_label, extra_context)
        self.set_default_changelist_filters(response.context_data['app_list'])
        return response


class ModelAdminDefaultFilterMixin:
    """
    A mixin for classes that inherit from django.contrib.admin.ModelAdmin.
    It augments the default changelist URL with filters defined on the class
    as "default_filters", which should be a dictionary mapping filter field
    names to values e.g. {'name__exact': 'name'}
    """

    @classmethod
    def get_default_changelist_url(self, model, query_filters):
        return '{path}?{query}'.format(
            path=reverse_lazy('admin:%s_%s_changelist' % (
                model._meta.app_label,
                model._meta.model_name)),
            query=urlencode(query_filters))

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['changelist_url'] = self.get_default_changelist_url(
            self.model,
            self.default_filters)

        return super().add_view(request,
                                form_url,
                                extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['changelist_url'] = self.get_default_changelist_url(
            self.model,
            self.default_filters)

        return super().change_view(request,
                                   object_id,
                                   form_url,
                                   extra_context=extra_context)
