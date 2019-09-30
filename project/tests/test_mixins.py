import copy
from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.test import SimpleTestCase
from ..mixins import AdminSiteDefaultFilterMixin, ModelAdminDefaultFilterMixin
from ..models import Project, Charge

# Simple matcher for a URL path with query parameters e.g.
# /admin/APP_NAME/MODEL_NAME?PARAM=VALUE
# From start to finish:
#   1. Match one or more path segments that start with '/' and may have alphanumeric and/or unreserved characters.
#   2. Match an optional trailing '/' after the last path segment
#   3. Match the '?' character indicating the start of the query portion of the URL
#   4. Match a query of the form 'key=value'. The key and value can have alphanumeric and/or unreserved characters. The value may have encoded characters as well.
#   5. Match one or more additional queries of the form 'key=value' that start with the '&' character, with the same stipulations as step 4.
URL_REGEX = r'^(\/[A-Za-z0-9-_.~]+)+\/?\?[A-Za-z0-9-_.~]+=([A-Za-z0-9-_.~]|(%[A-Za-z0-9]{2}))+(&[A-Za-z0-9-_.~]+=([A-Za-z0-9-_.~]|(%[A-Za-z0-9]{2}))+)*$'


class AdminSiteDefaultFilterMixinTestCase(SimpleTestCase):
    def test_sets_default_filter_url_in_template_context(self):
        test_context = {
            'app_list': [
                {
                    'app_label': 'test_app',
                    'models': [
                        {
                            'object_name': 'test_model',
                            'admin_url': '/admin/test/url'
                        }
                    ]
                }
            ]
        }

        class FakeAdminSite:
            def index(self, request, extra_context=None):
                return TemplateResponse(request,
                                        'fake_template_name.html',
                                        context=copy.deepcopy(test_context))

            def app_index(self, request, app_label, extra_context=None):
                return TemplateResponse(request,
                                        'fake_template_name.html',
                                        context=copy.deepcopy(test_context))

        class TestSite(AdminSiteDefaultFilterMixin, FakeAdminSite):
            default_filters = {
                'test_app.test_model': {'name__exact': 'name'}
            }

        testInstance = TestSite()

        response = testInstance.index(HttpRequest())
        app = next((app for app in response.context_data['app_list']
                    if app['app_label'] == 'test_app'))
        model = next((model for model in app['models']
                      if model['object_name'] == 'test_model'))
        self.assertRegex(model['admin_url'], URL_REGEX)

        response = testInstance.app_index(HttpRequest(), 'fake_app_label')
        app = next((app for app in response.context_data['app_list']
                    if app['app_label'] == 'test_app'))
        model = next((model for model in app['models']
                      if model['object_name'] == 'test_model'))
        self.assertRegex(model['admin_url'], URL_REGEX)


class ModelAdminDefaultFilterMixinTestCase(SimpleTestCase):
    def test_sets_default_filter_url_in_template_context(self):
        assertRegex = self.assertRegex

        class FakeModelAdmin:
            def add_view(self, request, form_url='', extra_context=None):
                assertRegex(extra_context['changelist_url'], URL_REGEX)

            def change_view(self, request, object_id, form_url='', extra_context=None):
                assertRegex(extra_context['changelist_url'], URL_REGEX)

        class TestAdmin(ModelAdminDefaultFilterMixin, FakeModelAdmin):
            pass

        testInstance = TestAdmin()

        testInstance.model = Project
        testInstance.default_filters = {'query_param': 'value'}
        testInstance.add_view(HttpRequest())
        testInstance.change_view(HttpRequest(), 0)

        testInstance.model = Charge
        testInstance.default_filters = {'query_param': 'value'}
        testInstance.add_view(HttpRequest())
        testInstance.change_view(HttpRequest(), 0)
