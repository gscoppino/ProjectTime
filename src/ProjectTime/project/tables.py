""" Defines the tables used by views in this app
"""

import django_tables2 as tables
from django.urls.base import reverse
from ProjectTime.project.models import Project, Charge


class ProjectTable(tables.Table):
    name = tables.Column(
        linkify=lambda record: reverse(
            'project:project-update',
            args=(record.pk,))
    )

    db_latest_charge = tables.DateTimeColumn(verbose_name='Latest Charge')

    class Meta:
        model = Project
        fields = ('name', 'active', 'db_latest_charge',)
        attrs = {'class': 'table stack hover'}
        empty_text = 'There are no projects.'


class ChargeTable(tables.Table):
    project = tables.Column(
        linkify=lambda record: reverse(
            'project:charge-update',
            args=(record.pk,))
    )

    db_time_charged = tables.Column(verbose_name='Time Charged')

    class Meta:
        model = Charge
        fields = ('project', 'start_time', 'end_time',
                  'db_time_charged', 'closed',)
        attrs = {'class': 'table stack hover'}
        empty_text = 'There are no charges.'
