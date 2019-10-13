from django.contrib import admin
from .constants import DEFAULT_PROJECT_CHANGELIST_FILTERS, DEFAULT_CHARGE_CHANGELIST_FILTERS
from .mixins import AdminSiteDefaultFilterMixin


class ProjectTimeAdminSite(AdminSiteDefaultFilterMixin, admin.AdminSite):
    site_title = 'ProjectTime'
    site_header = 'ProjectTime'
    index_title = 'ProjectTime Administration'
    default_filters = {
        'project.Project': DEFAULT_PROJECT_CHANGELIST_FILTERS,
        'project.Charge': DEFAULT_CHARGE_CHANGELIST_FILTERS
    }


admin_site = ProjectTimeAdminSite()
