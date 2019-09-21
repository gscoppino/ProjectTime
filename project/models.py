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

    name = models.CharField(
        unique=True,
        max_length=255,
        help_text='*Required: Enter a unique name for the project (255 characters max).')

    def __str__(self):
        return '%s' % (self.name)


class Task(models.Model):
    class Meta:
        ordering = ('deadline', 'done',)

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        help_text='*Required: Select the project this task will be associated with.')

    title = models.CharField(
        max_length=255,
        help_text='*Required: Enter the task that is to be done (255 characters max).')

    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Enter the date and time at which the task is to be done.')

    done = models.BooleanField(
        blank=True,
        default=False,
        help_text='A completed task is disabled for modification.')

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

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        help_text='*Required: Select the project this charge will be associated with.')

    start_time = models.DateTimeField(
        help_text='*Required: Enter the date and time that chargeable work began on.')

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Enter the date and time that chargeable work ended on.')

    closed = models.BooleanField(
        blank=True,
        default=False,
        help_text='A closed charge is disabled for modification.')

    @property
    def time_charged(self):
        if not self.end_time:
            return timedelta()

        return self.end_time - self.start_time

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if self.end_time and self.end_time < self.start_time:
            error = ValidationError(
                'The end time must not be before the start time.',
                code='end_time_must_be_on_or_after_start_time'
            )

            if exclude and 'end_time' in exclude:
                raise error
            else:
                raise ValidationError({'end_time': error})

        if self.closed and not self.end_time:
            error = ValidationError(
                'Cannot mark as closed without end time specified.',
                code='cannot_close_without_end_time'
            )

            if exclude and 'closed' in exclude:
                raise error
            else:
                raise ValidationError({'closed': error})

    def __str__(self):
        charged = self.time_charged

        return '{project}, {start_time} - {end_time} ({time_charged} {units}) [{status}]'.format(
            project=self.project.name,
            start_time=timezone.localtime(self.start_time),
            end_time=timezone.localtime(
                self.end_time) if self.end_time else '__:__:__',
            time_charged=charged,
            units='hours' if charged.total_seconds() >= 3600 else 'minutes',
            status='Closed' if self.closed else 'Open'
        )
