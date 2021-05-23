""" Defines mixins used in this app.
"""
import pandas as pd


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
