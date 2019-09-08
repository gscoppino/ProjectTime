from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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
        ordering = ('deadline', 'done',)

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '{project}: {task}{task_status}'.format(
            project=self.project.name,
            task=self.title,
            task_status=' (Completed)' if self.done else ' (due on %s)' % (
                timezone.localtime(self.deadline)) if self.deadline else ''
        )


class Charge(models.Model):
    objects = ChargeQuerySet.as_manager()

    class Meta:
        ordering = ('start_time',)
        get_latest_by = ('start_time',)
        constraints = (
            models.CheckConstraint(
                name='end_time_must_be_on_or_after_start_time',
                check=models.Q(end_time__gte=models.F('start_time'))
            ),
        )

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def time_charged(self):
        if not self.end_time:
            return timedelta()

        return self.end_time - self.start_time

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

        return '%s, %s - %s (%s %s)' % (
            self.project.name,
            timezone.localtime(self.start_time),
            timezone.localtime(self.end_time) if self.end_time else '__:__:__',
            charged,
            'hours' if charged.total_seconds() >= 3600 else 'minutes'
        )
