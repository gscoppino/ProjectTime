# pylint: disable=missing-function-docstring

from unittest.mock import patch

from django.contrib import admin
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.test.client import RequestFactory

from ProjectTime.project.site import ProjectTimeAdminSite


def get_mock_timezone_context(*args):
    return {'timezone': 'foo'}


class ProjectTimeAdminSiteTestCase(SimpleTestCase):
    def test_admin_site_sets_timezone_in_template_context(self):
        site = ProjectTimeAdminSite()
        request = RequestFactory().get('/foo/bar/')
        request.user = User()
        request.session = {'timezone': 'America/New_York'}

        context = site.each_context(request)
        self.assertIn('timezone', context)
        self.assertEqual(context['timezone'], 'America/New_York')

    @patch.object(admin.AdminSite, 'each_context', new=get_mock_timezone_context)
    def test_admin_site_raises_exception_when_timezone_unexpected_already_in_template_context(self):
        """ For example, if there is another key called "timezone" used by some other middleware.
        """
        site = ProjectTimeAdminSite()
        request = RequestFactory().get('/foo/bar')
        request.user = User()
        request.session = {'timezone': 'America/New_York'}

        with self.assertRaises(ValueError):
            site.each_context(request)
