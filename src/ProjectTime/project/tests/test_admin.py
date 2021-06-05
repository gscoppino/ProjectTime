# pylint: disable=missing-function-docstring

import types
from datetime import timedelta

from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from ProjectTime.project.admin import ChargeAdmin, ProjectAdmin
from ProjectTime.project.models import Charge, Project
from ProjectTime.project.site import admin_site


class ProjectModelAdminTestCase(TestCase):
    def setUp(self):
        self.model_admin = ProjectAdmin(model=Project, admin_site=admin_site)

    def test_project_admin_queryset_is_annotated_with_latest_charge(self):
        Project(name='Test').validate_and_save()
        Project(name='Test 2').validate_and_save()

        queryset = self.model_admin.get_queryset(HttpRequest())

        for project in queryset:
            self.assertTrue(hasattr(project, 'db_latest_charge'))

    def test_project_admin_list_display_contains_latest_charge(self):
        self.assertTrue('latest_charge' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db_latest_charge = timezone.now()
        self.assertEqual(self.model_admin.latest_charge(obj),
                         obj.db_latest_charge.date())

    def test_project_admin_list_display_when_no_charge(self):
        self.assertTrue('latest_charge' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db_latest_charge = None
        self.assertIsNone(self.model_admin.latest_charge(obj))

    def test_project_admin_latest_charge_field_is_sortable_in_list(self):
        self.assertTrue(hasattr(self.model_admin.latest_charge,
                                'admin_order_field'))
        self.assertEqual(
            self.model_admin.latest_charge.admin_order_field,
            'db_latest_charge'
        )

    def test_project_admin_has_all_fields_editable_when_creating_new_project(self):
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               None)
        self.assertEqual(len(readonly_fields), 0)

    def test_project_admin_has_all_fields_editable_when_project_is_active(self):
        project = Project(name='Test', active=True).validate_and_save()
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)
        self.assertEqual(len(readonly_fields), 0)

    def test_project_admin_has_read_only_project_name_when_project_is_not_active(self):
        project = Project(name='Test', active=False).validate_and_save()
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)

        self.assertSequenceEqual(readonly_fields, ('name',))


class ChargeModelAdminTestCase(TestCase):
    def setUp(self):
        self.project = Project(name='Test').validate_and_save()
        self.model_admin = ChargeAdmin(model=Charge, admin_site=admin_site)

    def test_charge_admin_date_hierarchy_is_set_to_start_time(self):
        # This property configures the admin to support browsing
        # through Charge records via a more granular date picker.
        self.assertEqual(self.model_admin.date_hierarchy, 'start_time')

    def test_charge_admin_queryset_is_annotated_with_time_charged(self):
        Charge(project=self.project,
               start_time=timezone.now()).validate_and_save()
        Charge(project=self.project,
               start_time=timezone.now()).validate_and_save()

        queryset = self.model_admin.get_queryset(HttpRequest())

        for charge in queryset:
            self.assertTrue(hasattr(charge, 'db_time_charged'))

    def test_charge_admin_list_display_contains_time_charged(self):
        self.assertTrue('time_charged' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db_time_charged = 'Test'
        self.assertEqual(self.model_admin.time_charged(obj), 'Test')

    def test_charge_admin_time_charged_field_is_sortable_in_list(self):
        self.assertTrue(hasattr(self.model_admin.time_charged,
                                'admin_order_field'))
        self.assertEqual(
            self.model_admin.time_charged.admin_order_field, 'db_time_charged'
        )

    def test_charge_admin_has_all_fields_editable_when_creating_new_charge(self):
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               None)

        self.assertEqual(len(readonly_fields), 0)

    def test_charge_admin_has_all_fields_editable_when_project_is_active_and_charge_is_not_closed(self):
        self.project.active = True
        self.project.validate_and_save()

        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        closed=False).validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertEqual(len(readonly_fields), 0)

    def test_charge_admin_has_read_only_start_and_end_time_when_project_not_active_and_charge_closed(self):
        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=1),
                        closed=True).validate_and_save()

        self.project.active = False
        self.project.validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields, ('start_time', 'end_time',))

    def test_charge_admin_has_read_only_start_time_end_time_and_project_when_charge_is_closed(self):
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

    def test_charge_admin_has_read_only_start_time_end_time_and_closed_status_when_project_not_active(self):
        charge = Charge(project=self.project,
                        start_time=timezone.now(),
                        closed=False).validate_and_save()

        self.project.active = False
        self.project.validate_and_save()

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields,
                                 ('start_time', 'end_time', 'closed',))
