from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ProjectAppConfig(AppConfig):
    name = 'ProjectTime.project'


class ProjectAdminConfig(AdminConfig):
    default_site = 'ProjectTime.project.site.ProjectTimeAdminSite'
