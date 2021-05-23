from unittest.mock import MagicMock, patch

import pandas as pd
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from ProjectTime.project.models import Project
from ProjectTime.project.site import ProjectTimeAdminSite
from ProjectTime.project.utils import reporting as report_helpers


def get_mock_admin_context():
    return MagicMock(return_value={'foo': 'bar'})


def get_mock_monthly_summary_dataframe():
    return MagicMock(return_value=pd.DataFrame())


def get_mock_monthly_summary_chart():
    return MagicMock(return_value=('script', '<div></div>'))


class AdminUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('test', '', 'test')

    # Helper methods
    def performLogin(self):
        logged_in = self.client.login(username='test', password='test')
        if not logged_in:
            self.fail('Unable to login.')


class ProjectTimeAdminSiteTimezoneFormViewTestCase(AdminUserTestCase):
    def test_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:select-timezone'))
        self.assertEqual(response.status_code, 302)

    def test_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:select-timezone'))
        self.assertEqual(response.status_code, 200)

    def test_timezone_form_template_is_used(self):
        self.client.get(reverse('admin:select-timezone'))
        self.assertTemplateUsed('timezone_form.html')

    def test_redirects_to_login_on_successful_submit(self):
        self.performLogin()
        response = self.client.post(reverse('admin:select-timezone'), {
            'timezone': 'America/New_York'
        })

        self.assertRedirects(
            response,
            reverse('admin:index'),
            fetch_redirect_response=False)


class ProjectTimeAdminSiteDashboardTemplateViewTestCase(AdminUserTestCase):
    def test_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_all_admin_context_is_available_on_context(self):
        self.performLogin()

        with patch.object(
            admin.AdminSite,
            'each_context',
            new_callable=get_mock_admin_context
        ):
            response = self.client.get(reverse('admin:dashboard'))

        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')

    def test_all_projects_are_selected_by_default(self):
        project_a = Project(name='Project A').validate_and_save()
        project_b = Project(name='Project B').validate_and_save()

        self.performLogin()

        response = self.client.get(reverse('admin:dashboard'))

        self.assertEqual(response.context['projects'], [
            {'id': project_a.pk, 'name': project_a.name, 'selected': True},
            {'id': project_b.pk, 'name': project_b.name, 'selected': True}
        ])

    def test_correct_projects_are_selected(self):
        project_a = Project(name='Project A').validate_and_save()
        project_b = Project(name='Project B').validate_and_save()

        self.performLogin()

        response = self.client.get('{url}?project={project}'.format(
            url=reverse('admin:dashboard'),
            project=project_a.pk
        ))

        self.assertEqual(response.context['projects'], [
            {'id': project_a.pk, 'name': project_a.name, 'selected': True},
            {'id': project_b.pk, 'name': project_b.name, 'selected': False}
        ])

    @patch.object(
        report_helpers,
        'get_monthly_summary_series',
        new_callable=get_mock_monthly_summary_dataframe
    )
    @patch.object(
        report_helpers,
        'get_monthly_summary_chart_components',
        new_callable=get_mock_monthly_summary_chart
    )
    def test_visualization_creation_blackbox(self, get_mock_dataframe, get_mock_chart_components):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertTrue(get_mock_dataframe.called)
        self.assertTrue(get_mock_chart_components.called)
        self.assertIn('chart_script', response.context)
        self.assertEqual(response.context['chart_script'], 'script')
        self.assertIn('chart_div', response.context)
        self.assertEqual(response.context['chart_div'], '<div></div>')
