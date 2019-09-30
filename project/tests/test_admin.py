import types
from datetime import timedelta
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone
from ..admin import ProjectAdmin, ChargeAdmin, admin_site
from ..models import Project, Charge
from .utils import validate_and_save


class ProjectModelAdminTestCase(TestCase):
    def setUp(self):
        self.model_admin = ProjectAdmin(model=Project, admin_site=admin_site)

    def test_changelist_shows_only_active_projects_by_default(self):
        self.assertEqual(self.model_admin.default_filters,
                         {'active__exact': 1})

    def test_change_form_template_is_overridden(self):
        self.assertEqual(self.model_admin.change_form_template,
                         'change_form.html')

    def test_queryset_is_annotated_with_latest_charge(self):
        validate_and_save(Project(name='Test'))
        validate_and_save(Project(name='Test 2'))

        qs = self.model_admin.get_queryset(HttpRequest())

        for project in qs:
            self.assertTrue(hasattr(project, 'db__latest_charge'))

    def test_latest_charge_is_set_as_computed_field(self):
        self.assertTrue('latest_charge' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db__latest_charge = timezone.now()
        self.assertEqual(self.model_admin.latest_charge(obj),
                         timezone.now().date())
        obj.db__latest_charge = 'Test'

    def test_latest_charge_computed_field_has_ordering_specified(self):
        self.assertTrue(hasattr(self.model_admin.latest_charge,
                                'admin_order_field'))

    def test_all_change_fields_are_editable_when_creating_new_project(self):
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               None)
        self.assertEqual(len(readonly_fields), 0)

    def test_all_change_fields_are_editable_when_project_is_active(self):
        project = validate_and_save(Project(name='Test', active=True))
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)
        self.assertEqual(len(readonly_fields), 0)

    def test_project_name_is_read_only_when_project_is_not_active(self):
        project = validate_and_save(Project(name='Test', active=False))
        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest,
                                                               project)

        self.assertSequenceEqual(readonly_fields, ('name',))


class ChargeModelAdminTestCase(TestCase):
    def setUp(self):
        self.project = validate_and_save(Project(name='Test'))
        self.model_admin = ChargeAdmin(model=Charge, admin_site=admin_site)

    def test_changelist_shows_only_unclosed_charges_by_default(self):
        self.assertEqual(self.model_admin.default_filters,
                         {'closed__exact': 0})

    def test_date_hierarchy_is_set_to_start_time(self):
        # This property configures the admin to support browsing
        # through Charge records via a more granular date picker.
        self.assertEqual(self.model_admin.date_hierarchy, 'start_time')

    def test_change_list_template_is_overridden(self):
        self.assertEqual(self.model_admin.change_list_template,
                         'charge_change_list.html')

    def test_change_form_template_is_overridden(self):
        self.assertEqual(self.model_admin.change_form_template,
                         'change_form.html')

    def test_queryset_is_annotated_with_time_charged(self):
        validate_and_save(Charge(project=self.project,
                                 start_time=timezone.now()))
        validate_and_save(Charge(project=self.project,
                                 start_time=timezone.now()))

        qs = self.model_admin.get_queryset(HttpRequest())

        for charge in qs:
            self.assertTrue(hasattr(charge, 'db__time_charged'))

    def test_time_charged_is_set_as_computed_field(self):
        self.assertTrue('time_charged' in self.model_admin.list_display)
        obj = types.SimpleNamespace()
        obj.db__time_charged = 'Test'
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
        validate_and_save(self.project)

        charge = validate_and_save(Charge(project=self.project,
                                          start_time=timezone.now(),
                                          closed=False))

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertEqual(len(readonly_fields), 0)

    def test_charge_start_time_and_end_time_are_read_only_when_project_is_not_active_and_charge_is_closed(self):
        charge = validate_and_save(Charge(project=self.project,
                                          start_time=timezone.now(),
                                          end_time=timezone.now() + timedelta(hours=1),
                                          closed=True))

        self.project.active = False
        validate_and_save(self.project)

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields, ('start_time', 'end_time',))

    def test_charge_start_time_end_time_and_project_are_read_only_when_charge_is_closed(self):
        self.project.active = True
        validate_and_save(self.project)

        charge = validate_and_save(Charge(project=self.project,
                                          start_time=timezone.now(),
                                          end_time=timezone.now() + timedelta(hours=1),
                                          closed=True))

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields,
                                 ('start_time', 'end_time', 'project',))

    def test_charge_start_time_end_time_and_closed_status_are_read_only_when_project_is_not_active(self):
        charge = validate_and_save(Charge(project=self.project,
                                          start_time=timezone.now(),
                                          closed=False))

        self.project.active = False
        validate_and_save(self.project)

        readonly_fields = self.model_admin.get_readonly_fields(HttpRequest(),
                                                               charge)

        self.assertSequenceEqual(readonly_fields,
                                 ('start_time', 'end_time', 'closed',))
