from django.db import models


class ChargeQuerySet(models.QuerySet):
    @staticmethod
    def get_time_charged_expr():
        return models.F('end_time') - models.F('start_time')

    def annotate_time_charged(self):
        return self.annotate(
            db__time_charged=ChargeQuerySet.get_time_charged_expr()
        )

    def aggregate_time_charged(self):
        return self.annotate_time_charged().aggregate(
            total_time_charged=models.Sum('db__time_charged')
        ).get('total_time_charged')
