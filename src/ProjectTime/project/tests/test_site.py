from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.test.client import RequestFactory

from ProjectTime.project.mixins import AdminSiteDefaultFilterMixin
from ProjectTime.project.site import ProjectTimeAdminSite


def get_mock_timezone_context(*args):
    return {'timezone': 'foo'}


class ProjectTimeAdminSiteTestCase(SimpleTestCase):
    def test_sets_timezone_in_context(self):
        site = ProjectTimeAdminSite()
        request = RequestFactory().get('/foo/bar/')
        request.user = User()
        request.session = {'timezone': 'America/New_York'}

        context = site.each_context(request)
        self.assertIn('timezone', context)
        self.assertEqual(context['timezone'], 'America/New_York')

    @patch.object(AdminSiteDefaultFilterMixin, 'each_context', new=get_mock_timezone_context)
    def test_raises_exception_on_key_conflict(self):
        site = ProjectTimeAdminSite()
        request = RequestFactory().get('/foo/bar')
        request.user = User()
        request.session = {'timezone': 'America/New_York'}

        with self.assertRaises(ValueError):
            site.each_context(request)
