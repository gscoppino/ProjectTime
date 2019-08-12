from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta
from .querysets import ProjectQuerySet, ChargeQuerySet

# Create your models here.


class Project(models.Model):
    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ('name',)

    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return '%s' % (self.name)


class Task(models.Model):
    class Meta:
        ordering = ('date', 'done',)

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    date = models.DateField()
    done = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '%s on %s: %s' % (
            self.project.name,
            self.date,
            self.title + ' (Completed)' if self.done else self.title
        )


class Charge(models.Model):
    objects = ChargeQuerySet.as_manager()

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
        charged = self.time_charged

        return '%s on %s, %s - %s (%s %s)' % (
            self.project.name,
            self.date,
            self.start_time,
            self.end_time or '__:__:__',
            charged,
            'hours' if charged.total_seconds() >= 3600 else 'minutes'
        )
