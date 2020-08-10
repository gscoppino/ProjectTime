""" Django app for managing projects and time spent on them.
"""

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ProjectAppConfig(AppConfig):
    """ App config for project Django app
    """
    name = 'ProjectTime.project'


class ProjectAdminConfig(AdminConfig):
    """ Custom admin for the project Django app
    """
    default_site = 'ProjectTime.project.site.ProjectTimeAdminSite'
