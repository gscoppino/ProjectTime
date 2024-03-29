# pylint: disable=missing-function-docstring

from unittest.mock import MagicMock, patch

import pandas as pd
from django.contrib import admin
from django.shortcuts import reverse

from ProjectTime.project.models import Project
from ProjectTime.project.utils import reporting as report_helpers
from ProjectTime.project.tests.utils.testcase import AdminUserTestCase


def get_mock_admin_context():
    return MagicMock(return_value={'foo': 'bar'})


def get_mock_monthly_summary_dataframe():
    return MagicMock(return_value=pd.DataFrame())


def get_mock_monthly_summary_chart():
    return MagicMock(return_value=('script', '<div></div>'))


class ProjectTimeAdminSiteTimezoneFormViewTestCase(AdminUserTestCase):
    def test_timezone_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:select-timezone'))
        self.assertEqual(response.status_code, 302)

    def test_timezone_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:select-timezone'))
        self.assertEqual(response.status_code, 200)

    def test_timezone_view_template_is_used(self):
        self.client.get(reverse('admin:select-timezone'))
        self.assertTemplateUsed('timezone_form.html')

    def test_timezone_view_redirects_to_login_on_successful_submit(self):
        self.performLogin()
        response = self.client.post(reverse('admin:select-timezone'), {
            'timezone': 'America/New_York'
        })

        self.assertRedirects(
            response,
            reverse('admin:index'),
            fetch_redirect_response=False)


class ProjectTimeAdminSiteDashboardTemplateViewTestCase(AdminUserTestCase):
    def test_dashboard_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_has_all_admin_context(self):
        self.performLogin()

        with patch.object(
            admin.AdminSite,
            'each_context',
            new_callable=get_mock_admin_context
        ):
            response = self.client.get(reverse('admin:dashboard'))

        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')

    def test_dashboard_view_has_all_projects_selected_unless_otherwise_specified(self):
        project_a = Project(name='Project A').validate_and_save()
        project_b = Project(name='Project B').validate_and_save()

        self.performLogin()

        response = self.client.get(reverse('admin:dashboard'))

        self.assertEqual(response.context['projects'], [
            {'id': project_a.pk, 'name': project_a.name, 'selected': True},
            {'id': project_b.pk, 'name': project_b.name, 'selected': True}
        ])

    def test_dashboard_view_has_correct_projects_selected_based_on_request_params(self):
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
    def test_dashboard_view_adds_chart_visualization_elements_to_template_context(
        self, get_mock_dataframe, get_mock_chart_components
    ):
        """ This is more of a black box test, the report helpers
            are tested in more detail in their dedicated suite
        """
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertTrue(get_mock_dataframe.called)
        self.assertTrue(get_mock_chart_components.called)
        self.assertIn('chart_script', response.context)
        self.assertEqual(response.context['chart_script'], 'script')
        self.assertIn('chart_div', response.context)
        self.assertEqual(response.context['chart_div'], '<div></div>')
