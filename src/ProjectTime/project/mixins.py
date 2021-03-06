""" Defines mixins used in this app.
"""
import pandas as pd

from .utils.urls import get_changelist_url


class ValidateModelMixin:  # pylint: disable=too-few-public-methods
    """ A mixin for classes that inherit from django.db.models.Models.
        It augments the model with a method that performs validation
        before saving changes.
    """

    def validate_and_save(self, *args, full_clean__exclude=None, **kwargs):
        """ Validate and save changes to the model instance.
            Returns the model instance afterwards, so can be used like so:
            ```
            model_instance = AModel(field=value, f2=v2).validate_and_save()
            ```
            Fields to be excluded from validation can be passed like so:
            ```
            model_instance.validate_and_save(full_clean__exclude=('f2))
            ```
        """
        self.full_clean(exclude=full_clean__exclude)
        self.save(*args, **kwargs)
        return self


class PandasQuerySetMixin:  # pylint: disable=too-few-public-methods
    """ A mixin for classes that inherit from django.db.models.QuerySet.
        It augments the queryset with a method that refines the queryset
        similarly to values_list, then evaluates and outputs a Pandas
        DataFrame.
    """

    def to_pandas(self, *values):
        return pd.DataFrame(list(self.values_list(*values, named=True)))


class AdminSiteDefaultFilterMixin:
    """
    A mixin for classes that inherit from django.contrib.admin.AdminSite
    It augments the default changelist URL's with filters defined on the class
    as "default_filters", which should be a dictionary mapping app models
    to a dictionary that maps filter field names to values e.g.
    {'test_app.test_model': {'name__exact': 'name'}}
    """

    @classmethod
    def set_default_changelist_filters(cls, app_list, filters):
        for app in app_list:
            for model in app['models']:
                option = '{app}.{model}'.format(app=app['app_label'],
                                                model=model['object_name'])

                if filters[option] is not None:
                    model['admin_url'] = get_changelist_url(
                        app['app_label'],
                        model['object_name'].lower(),
                        filters[option])

    def each_context(self, request):
        context = super().each_context(request)
        self.set_default_changelist_filters(context['available_apps'],
                                            self.default_filters)
        return context

    def index(self, request, extra_context=None):
        response = super().index(request, extra_context)
        self.set_default_changelist_filters(response.context_data['app_list'],
                                            self.default_filters)
        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super().app_index(request, app_label, extra_context)
        self.set_default_changelist_filters(response.context_data['app_list'],
                                            self.default_filters)
        return response


class ModelAdminDefaultFilterMixin:
    """
    A mixin for classes that inherit from django.contrib.admin.ModelAdmin.
    It augments the default changelist URL with filters defined on the class
    as "default_filters", which should be a dictionary mapping filter field
    names to values e.g. {'name__exact': 'name'}
    """

    def add_changelist_url_to_context(self, context):
        context['changelist_url'] = get_changelist_url(
            self.model._meta.app_label,  # pylint: disable=protected-access
            self.model._meta.model_name,  # pylint: disable=protected-access
            self.default_filters)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        self.add_changelist_url_to_context(extra_context)
        return super().add_view(request,
                                form_url,
                                extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        self.add_changelist_url_to_context(extra_context)
        return super().change_view(request,
                                   object_id,
                                   form_url,
                                   extra_context=extra_context)
