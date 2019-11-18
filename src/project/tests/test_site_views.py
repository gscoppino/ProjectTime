import pandas as pd
from datetime import timedelta
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.utils import timezone
from unittest.mock import MagicMock, patch
from ..models import Project
from ..site import ProjectTimeAdminSite
from .utils.general import validate_and_save
from .utils.charge import ChargeFactory


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


class ProjectTimeAdminSiteDashboardTemplateViewTestCase(AdminUserTestCase):
    def test_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertEqual(response.status_code, 200)

    @patch.object(AdminSite, 'each_context', new_callable=get_mock_admin_context)
    def test_all_admin_context_is_available_on_context(self, mock_method):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')

    def test_all_projects_are_selected_by_default(self):
        project_a = validate_and_save(Project(name='Project A'))
        project_b = validate_and_save(Project(name='Project B'))

        self.performLogin()

        response = self.client.get(reverse('admin:dashboard'))

        self.assertEqual(response.context['projects'], [
            {'id': project_a.pk, 'name': project_a.name, 'selected': True},
            {'id': project_b.pk, 'name': project_b.name, 'selected': True}
        ])

    def test_correct_projects_are_selected(self):
        project_a = validate_and_save(Project(name='Project A'))
        project_b = validate_and_save(Project(name='Project B'))

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
        project_a = validate_and_save(Project(name='Project A'))
        project_b = validate_and_save(Project(name='Project B'))

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
            validate_and_save(ChargeFactory.today(
                project=project_a,
                charge_time=charge
            ))

        for charge in project_b_current_charges:
            validate_and_save(ChargeFactory.today(
                project=project_b,
                charge_time=charge
            ))

        # Create charges in a past month

        validate_and_save(ChargeFactory.past_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ))

        validate_and_save(ChargeFactory.past_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ))

        # Create charges in a future month

        validate_and_save(ChargeFactory.future_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ))

        validate_and_save(ChargeFactory.future_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ))

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