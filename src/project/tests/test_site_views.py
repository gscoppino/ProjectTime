from datetime import timedelta
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.utils.duration import duration_iso_string
from django.utils import timezone
from unittest.mock import patch
from ..models import Project
from .utils.general import validate_and_save
from .utils.charge import ChargeFactory


def get_mock_admin_context(self, request):
    return {'foo': 'bar'}


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

    @patch.object(AdminSite, 'each_context', new=get_mock_admin_context)
    def test_all_admin_context_is_available_on_context(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')

    def test_all_projects_are_available_on_context(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard'))
        self.assertQuerysetEqual(response.context['projects'],
                                 Project.objects.all())


class ProjectAdminSiteDashboardJsonViewTestCase(AdminUserTestCase):
    def test_view_redirects_when_user_is_not_admin(self):
        response = self.client.get(reverse('admin:dashboard-data'))
        self.assertEqual(response.status_code, 302)

    def test_view_is_ok_when_user_is_admin(self):
        self.performLogin()
        response = self.client.get(reverse('admin:dashboard-data'))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_projects_with_total_charges_for_current_month(self):
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

        self.performLogin()

        # Should return data on all projects

        response = self.client.get(reverse('admin:dashboard-data'))
        self.assertJSONEqual(response.content, [
            {'project': project_a.pk,
             'project_name': 'Project A',
             'total_time_charged': duration_iso_string(
                 sum(project_a_current_charges,
                     timedelta()))},
            {'project': project_b.pk,
             'project_name': 'Project B',
             'total_time_charged': duration_iso_string(
                 sum(project_b_current_charges,
                     timedelta()))}
        ])

        # Should return data on only the requested projects

        response = self.client.get('{url}?project={project}'.format(
            url=reverse('admin:dashboard-data'),
            project=project_a.pk
        ))

        self.assertJSONEqual(response.content, [
            {'project': project_a.pk,
             'project_name': 'Project A',
             'total_time_charged': duration_iso_string(
                 sum(project_a_current_charges,
                     timedelta()))}
        ])
