from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from ProjectTime.project.models import Charge, Project

from .utils.charge import ChargeFactory


class CLITest(TestCase):
    def tearDown(self):
        # for some reason, the timezone is not deactivated after the tests
        timezone.deactivate()

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_lists_active_projects(self):
        Project(name="Test Active Project", active=True).validate_and_save()
        Project(name="Test Inactive Project", active=False).validate_and_save()

        out = StringIO()
        call_command('ls', 'projects', stdout=out)
        self.assertIn('Test Active Project', out.getvalue())
        self.assertNotIn('Test Inactive Project', out.getvalue())

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_lists_all_projects(self):
        Project(name="Test Active Project", active=True).validate_and_save()
        Project(name="Test Inactive Project", active=False).validate_and_save()

        out = StringIO()
        call_command('ls', 'projects', all=True, stdout=out)
        self.assertIn('Test Active Project', out.getvalue())
        self.assertIn('Test Inactive Project', out.getvalue())

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_renames_project(self):
        Project(name="Test Project").validate_and_save()
        new_name = "Renamed Project"
        self.assertTrue(Project.objects.filter(name="Test Project").exists())
        self.assertFalse(Project.objects.filter(name=new_name).exists())

        out = StringIO()
        call_command('rename', "Test Project", "Renamed Project", stdout=out)
        self.assertFalse(Project.objects.filter(name="Test Project").exists())
        self.assertTrue(Project.objects.filter(name=new_name).exists())

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_sets_project_active(self):
        self.assertEqual(Project.objects.count(), 0)
        Project(name="Test", active=False).validate_and_save()
        self.assertEqual(Project.objects.count(), 1)
        self.assertFalse(Project.objects.first().active)

        out = StringIO()
        call_command('set-active', 'Test', stdout=out)
        self.assertTrue(Project.objects.count(), 1)
        self.assertTrue(Project.objects.first().active)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_sets_project_inactive(self):
        self.assertEqual(Project.objects.count(), 0)
        Project(name="Test", active=True).validate_and_save()
        self.assertEqual(Project.objects.count(), 1)
        self.assertTrue(Project.objects.first().active)

        out = StringIO()
        call_command('set-inactive', 'Test', stdout=out)

        self.assertEqual(Project.objects.count(), 1)
        self.assertFalse(Project.objects.first().active)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_removes_project(self):
        Project(name="Test Project").validate_and_save()
        self.assertTrue(Project.objects.filter(name="Test Project").exists())

        out = StringIO()
        call_command('rm', "Test Project", stdout=out)
        self.assertFalse(Project.objects.filter(name="Test Project").exists())

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_list_open_charges(self):
        project = Project(name="Test Project").validate_and_save()

        open_charge = ChargeFactory.today(
            project=project, charge_time=timedelta(minutes=30))
        open_charge.validate_and_save()

        closed_charge = ChargeFactory.today(
            project=project, charge_time=timedelta(hours=1, minutes=45))
        closed_charge.closed = True
        closed_charge.validate_and_save()

        out = StringIO()
        call_command('ls', 'charges', stdout=out)
        result = out.getvalue()

        self.assertEqual(result.count("Test Project"), 1)
        self.assertIn("00:30:00 | False", result)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_list_all_charges(self):
        project = Project(name="Test Project").validate_and_save()

        open_charge = ChargeFactory.today(
            project=project, charge_time=timedelta(minutes=30))
        open_charge.validate_and_save()

        closed_charge = ChargeFactory.today(
            project=project, charge_time=timedelta(hours=1, minutes=45))
        closed_charge.closed = True
        closed_charge.validate_and_save()

        out = StringIO()
        call_command('ls', 'charges', all=True, stdout=out)
        result = out.getvalue()

        self.assertEqual(result.count("Test Project"), 2)
        self.assertIn("01:45:00 | True", result)
        self.assertIn("00:30:00 | False", result)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_makes_project(self):
        queryset = Project.objects.filter(name="Test")
        self.assertFalse(queryset.exists())

        out = StringIO()
        call_command('mkproject', 'Test', stdout=out)
        self.assertTrue(queryset.exists())
        self.assertEqual(queryset.count(), 1)

        project = queryset.first()
        self.assertEqual(project.name, 'Test')
        self.assertEqual(project.active, True)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_makes_open_charge_at_current_time(self):
        project = Project(name="Test").validate_and_save()

        queryset = Charge.objects.filter(project__name="Test")
        self.assertFalse(queryset.exists())

        out = StringIO()
        call_command('mkcharge', 'Test', stdout=out)
        self.assertTrue(queryset.exists())
        self.assertEqual(queryset.count(), 1)

        charge = queryset.first()
        self.assertEqual(charge.project.name, "Test")
        self.assertLess(
            timezone.now() - charge.start_time,
            timedelta(seconds=5)
        )
        self.assertEqual(charge.end_time, None)
        self.assertEqual(charge.closed, False)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_commits_end_time_to_latest_open_charge(self):
        project = Project(name="Test").validate_and_save()

        now = timezone.now()

        older_open_charge = Charge(
            project=project,
            start_time=now
        ).validate_and_save()

        now = timezone.now()

        newer_open_charge = Charge(
            project=project,
            start_time=now
        ).validate_and_save()

        now = timezone.now()
        closed_charge_end_time = now+timedelta(hours=1)

        newest_closed_charge = Charge(
            project=project,
            start_time=now,
            end_time=closed_charge_end_time,
            closed=True
        ).validate_and_save()

        self.assertTrue(Charge.objects.filter(project__name="Test").count(), 3)

        now = timezone.now()
        out = StringIO()
        call_command("commit", stdout=out)

        self.assertTrue(Charge.objects.filter(project__name="Test").count(), 3)
        older_open_charge.refresh_from_db()
        newer_open_charge.refresh_from_db()
        newest_closed_charge.refresh_from_db()

        self.assertIsNone(older_open_charge.end_time)
        self.assertIsNotNone(newer_open_charge.end_time)
        self.assertLessEqual(
            newer_open_charge.end_time - timezone.now(), timedelta(seconds=5)
        )
        self.assertEqual(newest_closed_charge.end_time, closed_charge_end_time)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_closes_latest_open_charge(self):
        project = Project(name="Test").validate_and_save()

        now = timezone.now()

        older_open_charge = Charge(
            project=project,
            start_time=now,
            end_time=now+timedelta(hours=1)
        ).validate_and_save()

        now = timezone.now()

        newer_open_charge = Charge(
            project=project,
            start_time=now,
            end_time=now+timedelta(hours=1)
        ).validate_and_save()

        out = StringIO()
        call_command('close', stdout=out)

        older_open_charge.refresh_from_db()
        newer_open_charge.refresh_from_db()

        self.assertFalse(older_open_charge.closed)
        self.assertTrue(newer_open_charge.closed)

    @override_settings(PROJECT_TIME_CLI_TIMEZONE="America/New_York")
    def test_removes_latest_open_charge(self):
        project = Project(name="Test").validate_and_save()

        now = timezone.now()

        older_open_charge = Charge(
            project=project,
            start_time=now,
            end_time=now + timedelta(seconds=1)
        ).validate_and_save()

        now = timezone.now()

        newer_open_charge = Charge(
            project=project,
            start_time=now,
            end_time=now + timedelta(seconds=1)
        ).validate_and_save()

        now = timezone.now()

        newest_closed_charge = Charge(
            project=project,
            start_time=now,
            end_time=now+timedelta(minutes=1),
            closed=True
        ).validate_and_save()

        self.assertTrue(Charge.objects.filter(project__name="Test").count(), 3)

        out = StringIO()
        call_command("rmcharge", stdout=out)

        self.assertTrue(Charge.objects.filter(project__name="Test").count(), 2)

        self.assertFalse(
            Charge.objects.filter(pk=newer_open_charge.pk).exists()
        )
        self.assertTrue(
            Charge.objects.filter(pk=older_open_charge.pk).exists()
        )
        self.assertTrue(
            Charge.objects.filter(pk=newest_closed_charge.pk).exists()
        )
