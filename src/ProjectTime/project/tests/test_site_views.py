from datetime import timedelta
from unittest.mock import MagicMock, patch

import pandas as pd
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.utils import timezone

from ProjectTime.project.models import Charge, Project
from ProjectTime.project.site import ProjectTimeAdminSite

from .utils.charge import ChargeFactory
from .utils.general import get_start_of_today


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
        ProjectTimeAdminSite,
        'get_monthly_summary_series',
        new_callable=get_mock_monthly_summary_dataframe
    )
    @patch.object(
        ProjectTimeAdminSite,
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

    def test_visualization_creation_whitebox(self):
        project_a = Project(name='Project A').validate_and_save()
        project_b = Project(name='Project B').validate_and_save()

        # Create some test charges in the current month

        project_a_current_charges = [
            timedelta(hours=4),
            timedelta(hours=4),
        ]

        project_b_current_charges = [
            timedelta(hours=4),
            timedelta(hours=4),
        ]

        for charge in project_a_current_charges:
            ChargeFactory.today(
                project=project_a,
                charge_time=charge
            ).validate_and_save()

        for charge in project_b_current_charges:
            ChargeFactory.today(
                project=project_b,
                charge_time=charge
            ).validate_and_save()

        # Create some unclosed charges in the current month
        Charge(
            project=project_a,
            start_time=get_start_of_today()
        ).validate_and_save()

        Charge(
            project=project_b,
            start_time=get_start_of_today()
        ).validate_and_save()

        # Create charges in a past month

        ChargeFactory.past_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        ChargeFactory.past_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        # Create charges in a future month

        ChargeFactory.future_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        ChargeFactory.future_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        site = ProjectTimeAdminSite()

        # Should return data on all projects

        dataframe = site.get_monthly_summary_series(timezone.localtime())

        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(len(dataframe), 2)

        self.assertIsInstance(dataframe['charge'], pd.Series)
        self.assertIsInstance(dataframe['value'], pd.Series)
        self.assertIsInstance(dataframe['angle'], pd.Series)
        self.assertIsInstance(dataframe['color'], pd.Series)

        project_a_dataframe = dataframe[dataframe.charge == project_a.name]
        project_b_dataframe = dataframe[dataframe.charge == project_b.name]

        self.assertFalse(project_a_dataframe.empty)
        self.assertFalse(project_b_dataframe.empty)

        self.assertEqual(project_a_dataframe.iloc[0].value, 8.0)
        self.assertEqual(project_b_dataframe.iloc[0].value, 8.0)

        self.assertIsInstance(project_a_dataframe.iloc[0].angle, float)
        self.assertIsInstance(project_b_dataframe.iloc[0].angle, float)

        self.assertIsInstance(project_a_dataframe.iloc[0].color, str)
        self.assertIsInstance(project_b_dataframe.iloc[0].color, str)

        div, chart = site.get_monthly_summary_chart_components(dataframe)
        self.assertGreater(len(div), 0)
        self.assertGreater(len(chart), 0)

        # Should return data on only the requested projects

        dataframe = site.get_monthly_summary_series(timezone.localtime(),
                                                    project_ids=[project_a.pk])

        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(len(dataframe), 1)

        self.assertIsInstance(dataframe['charge'], pd.Series)
        self.assertIsInstance(dataframe['value'], pd.Series)
        self.assertIsInstance(dataframe['angle'], pd.Series)
        self.assertIsInstance(dataframe['color'], pd.Series)

        self.assertEqual(dataframe.iloc[0].charge, project_a.name)
        self.assertEqual(dataframe.iloc[0].value, 8.0)
        self.assertIsInstance(dataframe.iloc[0].angle, float)
        self.assertIsInstance(dataframe.iloc[0].color, str)

        div, chart = site.get_monthly_summary_chart_components(dataframe)
        self.assertGreater(len(div), 0)
        self.assertGreater(len(chart), 0)
