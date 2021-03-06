import copy

from django.template.response import TemplateResponse
from django.test import SimpleTestCase
from django.test.client import RequestFactory

from ProjectTime.project.mixins import (AdminSiteDefaultFilterMixin,
                                        ModelAdminDefaultFilterMixin)
from ProjectTime.project.models import Charge, Project

# Simple matcher for a URL path with query parameters e.g.
# /admin/APP_NAME/MODEL_NAME?PARAM=VALUE
# From start to finish:
#   1. Match one or more path segments that start with '/' and may have alphanumeric and/or
#      unreserved characters.
#   2. Match an optional trailing '/' after the last path segment
#   3. Match the '?' character indicating the start of the query portion of the URL
#   4. Match a query of the form 'key=value'. The key and value can have alphanumeric and/or
#      unreserved characters. The value may have encoded characters as well.
#   5. Match one or more additional queries of the form 'key=value' that start with the '&'
#      character, with the same stipulations as step 4.
URL_REGEX = r'^(\/[A-Za-z0-9-_.~]+)+\/?\?[A-Za-z0-9-_.~]+=([A-Za-z0-9-_.~]|(%[A-Za-z0-9]{2}))+(&[A-Za-z0-9-_.~]+=([A-Za-z0-9-_.~]|(%[A-Za-z0-9]{2}))+)*$'


def get_fake_app_list():
    return [
        {
            'app_label': 'project',
            'models': [
                {
                    'object_name': 'Project',
                    'admin_url': '/admin/test/url'
                },
                {
                    'object_name': 'Charge',
                    'admin_url': '/admin/test/url'
                }
            ]
        }
    ]


class AdminSiteDefaultFilterMixinTestCase(SimpleTestCase):
    def test_set_default_changelist_urls_on_index_page_template_context(self):
        test_context = {
            'app_list': get_fake_app_list()
        }

        class FakeAdminSite:
            def index(self, request, *args, **kwargs):
                return TemplateResponse(
                    request,
                    'fake_template_name.html',
                    context=copy.deepcopy(test_context)
                )

        class TestSite(AdminSiteDefaultFilterMixin, FakeAdminSite):
            default_filters = {
                'project.Project': {'test__exact': 'test'},
                'project.Charge': {'test__exact': 'test'}
            }

        test_site = TestSite()

        response = test_site.index(RequestFactory().get('/foo/bar'))
        app = next((app for app in response.context_data['app_list']
                    if app['app_label'] == 'project'))

        project_model = next((model for model in app['models']
                              if model['object_name'] == 'Project'))
        charge_model = next((model for model in app['models']
                             if model['object_name'] == 'Charge'))

        self.assertRegex(project_model['admin_url'], URL_REGEX)
        self.assertRegex(charge_model['admin_url'], URL_REGEX)

    def test_set_default_changelist_urls_on_apps_page_template_context(self):
        test_context = {
            'app_list': get_fake_app_list()
        }

        class FakeAdminSite:
            def app_index(self, request, *args, **kwargs):
                return TemplateResponse(
                    request,
                    'fake_template_name.html',
                    context=copy.deepcopy(test_context)
                )

        class TestSite(AdminSiteDefaultFilterMixin, FakeAdminSite):
            default_filters = {
                'project.Project': {'test__exact': 'test'},
                'project.Charge': {'test__exact': 'test'}
            }

        test_site = TestSite()

        response = test_site.app_index(
            RequestFactory().get('/foo/bar'), 'fake_app_label'
        )
        app = next((app for app in response.context_data['app_list']
                    if app['app_label'] == 'project'))

        project_model = next((model for model in app['models']
                              if model['object_name'] == 'Project'))
        charge_model = next((model for model in app['models']
                             if model['object_name'] == 'Charge'))

        self.assertRegex(project_model['admin_url'], URL_REGEX)
        self.assertRegex(charge_model['admin_url'], URL_REGEX)

    def test_set_default_changelist_urls_on_template_context_for_nav_sidebar(self):
        class FakeAdminSite:
            def each_context(self, request):
                return {
                    'available_apps': get_fake_app_list()
                }

        class TestSite(AdminSiteDefaultFilterMixin, FakeAdminSite):
            default_filters = {
                'project.Project': {'test__exact': 'test'},
                'project.Charge': {'test__exact': 'test'}
            }

        test_site = TestSite()

        context = test_site.each_context(RequestFactory().get('/foo/bar'))
        app = next((app for app in context['available_apps']
                    if app['app_label'] == 'project'))

        project_model = next((model for model in app['models']
                              if model['object_name'] == 'Project'))
        charge_model = next((model for model in app['models']
                             if model['object_name'] == 'Charge'))

        self.assertRegex(project_model['admin_url'], URL_REGEX)
        self.assertRegex(charge_model['admin_url'], URL_REGEX)


class ModelAdminDefaultFilterMixinTestCase(SimpleTestCase):
    def test_sets_default_filter_url_in_template_context(self):
        assertRegex = self.assertRegex

        class FakeModelAdmin:
            def add_view(self, *args, extra_context=None, **kwargs):
                assertRegex(extra_context['changelist_url'], URL_REGEX)

            def change_view(self, *args, extra_context=None, **kwargs):
                assertRegex(extra_context['changelist_url'], URL_REGEX)

        class ProjectTestAdmin(ModelAdminDefaultFilterMixin, FakeModelAdmin):
            model = Project
            default_filters = {'query_param': 'value'}

        class ChargeTestAdmin(ModelAdminDefaultFilterMixin, FakeModelAdmin):
            model = Charge
            default_filters = {'query_param': 'value'}

        test_admin = ProjectTestAdmin()

        test_admin.add_view(RequestFactory().get('/foo/bar'))
        test_admin.change_view(RequestFactory().get('/foo/bar'), 0)

        test_admin = ChargeTestAdmin()

        test_admin.add_view(RequestFactory().get('/foo/bar'))
        test_admin.change_view(RequestFactory().get('/foo/bar'), 0)
