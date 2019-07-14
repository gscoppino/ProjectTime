from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta


# Create your models here.


class Project(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return '%s' % (self.name)


class Charge(models.Model):
    class Meta:
        ordering = ('date', 'start_time',)
        get_latest_by = ('date', 'start_time',)
        constraints = (
            models.CheckConstraint(
                name='end_time_must_be_on_or_after_start_time',
                check=models.Q(end_time__gte=models.F('start_time'))
            ),
        )

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    @property
    def time_charged(self):
        if not self.end_time:
            return timedelta()

        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time)

        return end_datetime - start_datetime

    def clean(self):
        if self.end_time and self.end_time < self.start_time:
            raise ValidationError({
                'end_time': ValidationError(
                    'The end time must not be before the start time.',
                    code='end_time_must_be_on_or_after_start_time'
                )
            })

    def __str__(self):
        return '%s on %s, %s - %s (%s %s)' % (
            self.project.name,
            self.date,
            self.start_time,
            self.end_time or '__:__:__',
            self.time_charged,
            'hours' if self.time_charged.total_seconds() >= 3600 else 'minutes'
        )
