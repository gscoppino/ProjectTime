from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ProjectAppConfig(AppConfig):
    name = 'project'


class ProjectAdminConfig(AdminConfig):
    default_site = 'project.site.ProjectTimeAdminSite'
