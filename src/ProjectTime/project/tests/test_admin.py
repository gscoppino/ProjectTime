import types
from datetime import timedelta

from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from ProjectTime.project.admin import ChargeAdmin, ProjectAdmin, admin_site
from ProjectTime.project.models import Charge, Project


class ProjectModelAdminTestCase(TestCase):
    def setUp(self):
        self.model_admin = ProjectAdmin(model=Project, admin_site=admin_site)

    def test_queryset_is_annotated_with_latest_charge(self):
        Project(name='Test').validate_and_save()
        Project(name='Test 2').validate_and_save()

        queryset = self.model_admin.get_queryset(HttpRequest())

        for project in queryset:
            self.assertTrue(hasattr(project, 'db_latest_charge'))

    def test_latest_charge_is_set_as_computed_field(self):
        self.assertTrue('latest_charge' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db_latest_charge = timezone.now()
        self.assertEqual(self.model_admin.latest_charge(obj),
                         timezone.now().date())
        obj.db_latest_charge = 'Test'

    def test_latest_charge_computed_field_has_ordering_specified(self):
        self.assertTrue(hasattr(self.model_admin.latest_charge,
                                'admin_order_field'))

    def test_all_change_fields_are_editable_when_creating_new_project(self):
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               None)
        self.assertEqual(len(readonly_fields), 0)

    def test_all_change_fields_are_editable_when_project_is_active(self):
        project = Project(name='Test', active=True).validate_and_save()
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)
        self.assertEqual(len(readonly_fields), 0)

    def test_project_name_is_read_only_when_project_is_not_active(self):
        project = Project(name='Test', active=False).validate_and_save()
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)

        self.assertSequenceEqual(readonly_fields, ('name',))


class ChargeModelAdminTestCase(TestCase):
    def setUp(self):
        self.project = Project(name='Test').validate_and_save()
        self.model_admin = ChargeAdmin(model=Charge, admin_site=admin_site)

    def test_date_hierarchy_is_set_to_start_time(self):
        # This property configures the admin to support browsing
        # through Charge records via a more granular date picker.
        self.assertEqual(self.model_admin.date_hierarchy, 'start_time')

    def test_queryset_is_annotated_with_time_charged(self):
        Charge(project=self.project,
               start_time=timezone.now()).validate_and_save()
        Charge(project=self.project,
               start_time=timezone.now()).validate_and_save()

        queryset = self.model_admin.get_queryset(HttpRequest())

        for charge in queryset:
            self.assertTrue(hasattr(charge, 'db_time_charged'))

    def test_time_charged_is_set_as_computed_field(self):
        self.assertTrue('time_charged' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db_time_charged = 'Test'
        self.assertEqual(self.model_admin.time_charged(obj), 'Test')

    def test_time_charged_computed_field_has_ordering_specified(self):
        self.assertTrue(hasattr(self.model_admin.time_charged,
                                'admin_order_field'))

    def test_all_change_fields_are_editable_when_creating_new_charge(self):
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               None)

        self.assertEqual(len(readonly_fields), 0)

    def test_all_change_fields_are_editable_when_project_is_active_and_charge_is_not_closed(self):
        self.project.active = True
        self.project.validate_and_save()

        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        closed=False).validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertEqual(len(readonly_fields), 0)

    def test_start_and_end_time_are_read_only_when_project_not_active_and_charge_closed(self):
        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=1),
                        closed=True).validate_and_save()

        self.project.active = False
        self.project.validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields, ('start_time', 'end_time',))

    def test_start_time_end_time_and_project_are_read_only_when_charge_is_closed(self):
        self.project.active = True
        self.project.validate_and_save()

        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=1),
                        closed=True).validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields,
                                 ('start_time', 'end_time', 'project',))

    def test_start_time_end_time_and_closed_status_are_read_only_when_project_not_active(self):
        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        closed=False).validate_and_save()

        self.project.active = False
        self.project.validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields,
                                 ('start_time', 'end_time', 'closed',))
