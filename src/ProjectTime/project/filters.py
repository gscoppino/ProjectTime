""" Defines the filters used by views in this app
"""

import django_filters as filters
from ProjectTime.project.models import Project, Charge


class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'name': ['icontains'],
            'active': ['exact'],
        }


class ChargeFilter(filters.FilterSet):
    class Meta:
        model = Charge
        fields = {
            'project': ['exact'],
            'project__name': ['icontains'],
            'start_time': ['date__exact'],
            'end_time': ['date__exact'],
            'closed': ['exact'],
        }
