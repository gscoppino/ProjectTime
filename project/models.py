from django.db import models
from datetime import datetime, timezone

# Create your models here.


class Project(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return '%s' % (self.name)


class Charge(models.Model):
    class Meta:
        ordering = ('date', 'start_time',)
        get_latest_by = ('date', 'start_time',)

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    @property
    def time_charged(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time or datetime.now(
            timezone.utc).time())

        return end_datetime - start_datetime

    def __str__(self):

        return '%s on %s, %s - %s (%s minutes)' % (
            self.project.name,
            self.date,
            self.start_time,
            self.end_time,
            self.time_charged
        )
