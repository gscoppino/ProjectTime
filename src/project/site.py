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

    def each_context(self, request):
        context = super().each_context(request)

        if context.get('timezone') is not None:
            raise ValueError('Timezone context key would conflict with an'
                             'existing key in the Django admin context.')

        context['timezone'] = request.session.get('timezone') or 'N/A'

        return context


admin_site = ProjectTimeAdminSite()
