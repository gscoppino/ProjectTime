from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from unittest.mock import patch
from ..models import Project

def get_mock_admin_context(self, request):
    return {'foo': 'bar'}

class ProjectTimeAdminSiteDashboardViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('test', '', 'test')

    def test_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_is_ok_when_user_is_admin(self):
        self.perform_login()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 200)

    @patch.object(AdminSite, 'each_context', new=get_mock_admin_context)
    def test_all_admin_context_is_available_on_context(self):
        self.perform_login()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')
    
    def test_all_projects_are_available_on_context(self):
        self.perform_login()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertQuerysetEqual(response.context['projects'],
                                 Project.objects.all())

    # Helper methods
    def perform_login(self):
        logged_in = self.client.login(username='test', password='test')
        if not logged_in:
            self.fail('Unable to login.')