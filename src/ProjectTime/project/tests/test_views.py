# pylint: disable=missing-function-docstring

from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from ProjectTime.project.models import Charge, Project
from ProjectTime.project.tests.utils.testcase import AdminUserTestCase


class ProjectTimeIndexViewTestCase(AdminUserTestCase):
    def test_index_view_is_ok(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_redirects_authenticated_user(self):
        self.performLogin()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)


class ProjectTimeDashboardViewTestCase(AdminUserTestCase):
    def test_dashboard_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_is_ok(self):
        self.performLogin()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class ProjectListViewTestCase(AdminUserTestCase):
    def test_project_list_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('project:project-list'))
        self.assertEqual(response.status_code, 302)

    def test_project_list_view_is_ok(self):
        self.performLogin()
        response = self.client.get(reverse('project:project-list'))
        self.assertEqual(response.status_code, 200)


class ProjectCreateViewTestCase(AdminUserTestCase):
    def test_project_create_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('project:project-create'))
        self.assertEqual(response.status_code, 302)

    def test_project_create_view_is_ok(self):
        self.performLogin()
        response = self.client.get(reverse('project:project-create'))
        self.assertEqual(response.status_code, 200)


class ProjectUpdateViewTestCase(AdminUserTestCase):
    def test_project_update_view_redirects_when_not_logged_in(self):
        project = Project(name='Test').validate_and_save()
        response = self.client.get(
            reverse('project:project-update',
                    args=(project.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_project_update_view_is_ok(self):
        self.performLogin()
        project = Project(name='Test').validate_and_save()
        response = self.client.get(
            reverse('project:project-update',
                    args=(project.pk,)))
        self.assertEqual(response.status_code, 200)


class ChargeListViewTestCase(AdminUserTestCase):
    def test_charge_list_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('project:charge-list'))
        self.assertEqual(response.status_code, 302)

    def test_charge_list_view_is_ok(self):
        self.performLogin()
        response = self.client.get(reverse('project:charge-list'))
        self.assertEqual(response.status_code, 200)


class ChargeCreateViewTestCase(AdminUserTestCase):
    def test_charge_create_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('project:charge-create'))
        self.assertEqual(response.status_code, 302)

    def test_charge_create_view_is_ok(self):
        self.performLogin()
        response = self.client.get(reverse('project:charge-create'))
        self.assertEqual(response.status_code, 200)

    def test_charge_create_view_time_resolution_defaults_to_minutes(self):
        self.performLogin()
        response = self.client.get(reverse('project:charge-create'))
        form = response.context['form']
        default_charge_start_time = form['start_time'].value()
        self.assertEqual(default_charge_start_time.second, 0)
        self.assertEqual(default_charge_start_time.microsecond, 0)


class ChargeUpdateViewTestCase(AdminUserTestCase):
    def test_charge_update_view_redirects_when_not_logged_in(self):
        now = timezone.now()
        project = Project(name='Test').validate_and_save()
        charge = Charge(project=project, start_time=now).validate_and_save()
        response = self.client.get(
            reverse('project:charge-update',
                    args=(charge.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_charge_update_view_is_ok(self):
        now = timezone.now()
        self.performLogin()
        project = Project(name='Test').validate_and_save()
        charge = Charge(project=project, start_time=now).validate_and_save()
        response = self.client.get(
            reverse('project:charge-update',
                    args=(charge.pk,)))
        self.assertEqual(response.status_code, 200)


class ChargeCloseViewTestCase(AdminUserTestCase):
    def test_charge_close_view_redirects_when_not_logged_in(self):
        now = timezone.now()
        end = now+timedelta(minutes=1)
        project = Project(name='Test').validate_and_save()
        charge = Charge(
            project=project,
            start_time=now,
            end_time=end
        ).validate_and_save()
        response = self.client.get(
            reverse('project:close-charge',
                    args=(charge.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_charge_close_view(self):
        now = timezone.now()
        end = now+timedelta(minutes=1)
        self.performLogin()
        project = Project(name='Test').validate_and_save()
        charge = Charge(
            project=project,
            start_time=now,
            end_time=end
        ).validate_and_save()
        response = self.client.post(
            reverse('project:close-charge',
                    args=(charge.pk,)))
        charge.refresh_from_db()
        self.assertTrue(charge.closed)
        self.assertEqual(response.status_code, 302)
