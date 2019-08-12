from django.db import models


class ProjectQuerySet(models.QuerySet):
    def annotate_open_task_count(self):
        return self.annotate(
            db__open_task_count=models.Count(
                'task', filter=models.Q(task__done=False), distinct=True
            )
        )

    def annotate_latest_charge(self):
        return self.annotate(
            db__latest_charge=models.Max('charge__date')
        )


class ChargeQuerySet(models.QuerySet):
    def annotate_time_charged(self):
        return self.annotate(
            db__time_charged=models.F('end_time') - models.F('start_time')
        )

    def aggregate_time_charged(self):
        return self.annotate_time_charged().aggregate(
            total_time_charged=models.Sum('db__time_charged')
        ).get('total_time_charged')
