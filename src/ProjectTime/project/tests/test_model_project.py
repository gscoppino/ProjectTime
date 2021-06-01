from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.test import TestCase, SimpleTestCase

from ProjectTime.project.models import Project
from ProjectTime.project.querysets import ProjectQuerySet
from ProjectTime.project.tests.utils.general import ValidationMixin, get_model_field


class SimpleProjectModelTestCase(ValidationMixin, SimpleTestCase):
    def test_project_name_field_has_explicit_domain_name(self):
        field = get_model_field(Project, 'name')
        self.assertEqual(field.verbose_name, 'name')

    def test_project_name_field_has_description(self):
        field = get_model_field(Project, 'name')
        self.assertGreater(len(field.help_text), 0)

    def test_project_name_field_cannot_exceed_255_characters(self):
        with self.assertRaises(ValidationError) as cm:
            Project(name=''.zfill(256)).full_clean()
            self.assertValidationMessagePresent(
                cm.exception.error_dict,
                field='name',
                error_code='max_length'
            )

    def test_project_active_field_has_explicit_domain_name(self):
        field = get_model_field(Project, 'active')
        self.assertEqual(field.verbose_name, 'active')

    def test_project_active_field_has_description(self):
        field = get_model_field(Project, 'active')
        self.assertGreater(len(field.help_text), 0)

    def test_project_active_field_is_not_required(self):
        active_field = get_model_field(Project, 'active')
        self.assertEqual(active_field.blank, True)

    def test_project_active_field_is_set_to_true_unless_otherwise_specified(self):
        active_field = get_model_field(Project, 'active')
        self.assertEqual(active_field.default, True)

    def test_project_has_descriptive_string_representation(self):
        project = Project(name='Test')
        self.assertEqual(str(project), 'Test')

        project.active = False
        self.assertEqual(str(project), 'Test (Inactive)')


class ProjectModelTestCase(ValidationMixin, TestCase):
    def test_project_model_has_custom_queryset_manager(self):
        self.assertQuerysetEqual(Project.objects.get_queryset(),
                                 ProjectQuerySet(model=Project))

    def test_project_can_be_created(self):
        test_name = 'Test'
        project = Project(name=test_name).validate_and_save()

        self.assertEqual(project.name, test_name)
        self.assertEqual(project.active, True)

    def test_project_name_cannot_exceed_255_characters_in_database(self):
        with self.assertRaises(DataError):
            Project.objects.create(name=''.zfill(256))

    def test_project_name_must_be_unique(self):
        test_name = 'Test'

        Project(name=test_name).validate_and_save()

        with self.assertRaises(ValidationError) as cm:
            Project(name=test_name).validate_and_save()
            self.assertValidationMessagePresent(
                cm.exception.error_dict,
                field='name',
                error_code='unique'
            )

    def test_project_name_must_be_unique_in_database(self):
        test_name = 'Test'

        Project(name=test_name).validate_and_save()
        with self.assertRaises(IntegrityError):
            Project.objects.create(name=test_name)

    def test_project_cannot_be_modified_when_inactive(self):
        project = Project(name='Test', active=False).validate_and_save()

        # Should raise a generic validation error if attempting to
        # save on a inactive project
        with self.assertRaises(ValidationError) as cm:
            project.validate_and_save()
            self.assertValidationMessagePresent(
                cm.exception.error_dict,
                field='__all__',
                error_code='cannot_modify_when_inactive'
            )

        # But should be able to save the change if it is
        # re-opening the project
        project.active = True
        project.validate_and_save()
        self.assertEqual(project.active, True)
