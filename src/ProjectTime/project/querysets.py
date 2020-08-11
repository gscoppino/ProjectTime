""" Defines custom QuerySet's used by models in this app
"""

from django.db import models

from .mixins import PandasQuerySetMixin


class ProjectQuerySet(models.QuerySet, PandasQuerySetMixin):
    """ Extra queryset methods for projects
    """

    def annotate_latest_charge(self):
        return self.annotate(
            db__latest_charge=models.Max('charge__end_time')
        )


class ChargeQuerySet(models.QuerySet, PandasQuerySetMixin):
    """ Extra queryset methods for charges
    """

    def annotate_time_charged(self):
        return self.annotate(
            db__time_charged=models.F('end_time') - models.F('start_time')
        )

    def aggregate_time_charged(self):
        return self.annotate_time_charged().aggregate(
            total_time_charged=models.Sum('db__time_charged')
        ).get('total_time_charged')
