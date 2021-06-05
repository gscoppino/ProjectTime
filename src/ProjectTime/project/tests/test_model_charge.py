from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from ProjectTime.project.models import Charge, Project
from ProjectTime.project.querysets import ChargeQuerySet
from ProjectTime.project.tests.utils.general import (ValidationMixin,
                                                     get_model_field)


class SimpleChargeModelTestCase(ValidationMixin, SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = Project(name='Test')

    def test_charge_project_field_has_explicit_domain_name(self):
        field = get_model_field(Charge, 'project')
        self.assertEqual(field.verbose_name, 'project')

    def test_charge_project_field_has_description(self):
        field = get_model_field(Charge, 'project')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_start_time_field_has_explicit_domain_name(self):
        field = get_model_field(Charge, 'start_time')
        self.assertEqual(field.verbose_name, 'start time')

    def test_charge_start_time_field_has_description(self):
        field = get_model_field(Charge, 'start_time')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_end_time_field_has_explicit_domain_name(self):
        field = get_model_field(Charge, 'end_time')
        self.assertEqual(field.verbose_name, 'end time')

    def test_charge_end_time_field_has_description(self):
        field = get_model_field(Charge, 'end_time')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_closed_field_has_explicit_domain_name(self):
        field = get_model_field(Charge, 'closed')
        self.assertEqual(field.verbose_name, 'closed')

    def test_charge_closed_field_has_description(self):
        field = get_model_field(Charge, 'closed')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_has_descriptive_string_representation(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(project=self.project, start_time=start_datetime)
        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - __:__:__ (0:00:00 minutes) [Open]')

        charge.end_time = start_datetime + timedelta(minutes=30)
        self.assertEqual(
            str(charge),
            'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 8:30 a.m. (0:30:00 minutes) [Open]'
        )

        charge.end_time = start_datetime + timedelta(hours=1)
        self.assertEqual(
            str(charge),
            'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9 a.m. (1:00:00 hours) [Open]'
        )

        charge.end_time = start_datetime + timedelta(hours=1, minutes=15)
        self.assertEqual(
            str(charge),
            'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9:15 a.m. (1:15:00 hours) [Open]'
        )

        charge.closed = True
        self.assertEqual(
            str(charge),
            'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9:15 a.m. (1:15:00 hours) [Closed]'
        )

    def test_charge_time_charged_property_returns_correct_time_charged(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))
        timedelta_zero = timedelta()
        added_time = timedelta(minutes=30)

        charge = Charge(project=self.project, start_time=start_datetime)
        self.assertEqual(charge.time_charged, timedelta_zero)

        charge.end_time = start_datetime + added_time
        self.assertEqual(charge.time_charged, added_time)


class ChargeModelTestCase(ValidationMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = Project(name='Test').validate_and_save()

    def test_charge_has_custom_queryset_manager(self):
        self.assertQuerysetEqual(Charge.objects.get_queryset(),
                                 ChargeQuerySet(model=Charge))

    def test_charge_can_be_created_today(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        timedelta_zero = timedelta()

        charge = Charge(
            project=self.project,
            start_time=today
        ).validate_and_save()

        self.assertIsNotNone(charge.pk)
        self.assertEqual(charge.project, self.project)
        self.assertEqual(charge.start_time, today)

    def test_charge_project_must_be_active_project(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        inactive_project = Project(
            name='Test 2',
            active=False
        ).validate_and_save()

        charge = Charge(
            project=inactive_project,
            start_time=start_datetime,
            end_time=start_datetime + timedelta(hours=1)
        )

        with self.assertRaises(ValidationError) as context_manager:
            charge.full_clean()

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='project',
            error_code='project_must_be_active'
        )

    def test_charge_end_time_field_is_not_required(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)

        Charge(
            project=self.project,
            start_time=today
        ).validate_and_save()

    def test_charge_end_time_field_defaults_to_null(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)

        charge = Charge(
            project=self.project,
            start_time=today
        ).validate_and_save()

        self.assertIsNone(charge.end_time)

    def test_charge_end_time_field_is_set_to_given_value(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        end_time = today + timedelta(minutes=1)
        charge = Charge(
            project=self.project,
            start_time=today,
            end_time=end_time
        ).validate_and_save()

        self.assertEqual(charge.end_time, end_time)

    def test_charge_closed_field_is_not_required(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)

        Charge(
            project=self.project,
            start_time=today
        ).validate_and_save()

    def test_charge_closed_field_defaults_to_false(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)

        charge = Charge(
            project=self.project,
            start_time=today
        ).validate_and_save()

        self.assertFalse(charge.closed)

    def test_charge_closed_field_is_set_to_given_value(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)

        charge = Charge(
            project=self.project,
            start_time=today,
            end_time=today+timedelta(minutes=1),
            closed=False
        ).validate_and_save()

        self.assertFalse(charge.closed)

        charge = Charge(
            project=self.project,
            start_time=today,
            end_time=today+timedelta(minutes=1),
            closed=True
        ).validate_and_save()

        self.assertTrue(charge.closed)

    def test_charge_cannot_be_created_with_end_time_before_start_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime,
            end_time=start_datetime - timedelta(minutes=1)
        )

        # Should raise a keyed validation error
        with self.assertRaises(ValidationError) as context_manager:
            charge.full_clean()

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='end_time',
            error_code='end_time_must_be_on_or_after_start_time'
        )

        # Should raise a generic validation error if the end time field
        # is excluded
        with self.assertRaises(ValidationError) as context_manager:
            charge.full_clean(exclude=('end_time',))

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='__all__',
            error_code='end_time_must_be_on_or_after_start_time'
        )

    def test_charge_cannot_be_created_with_end_time_before_start_time_database(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        with self.assertRaises(IntegrityError):
            Charge.objects.create(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1))

    def test_charge_cannot_be_closed_without_end_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime,
            closed=True
        )

        # Should raise a keyed validation error
        with self.assertRaises(ValidationError) as context_manager:
            charge.full_clean()

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='closed',
            error_code='cannot_close_without_end_time'
        )

        # Should raise a generic validation error if the end time field
        # is excluded
        with self.assertRaises(ValidationError) as context_manager:
            charge.full_clean(exclude=('closed',))

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='__all__',
            error_code='cannot_close_without_end_time'
        )

    def test_charge_cannot_be_closed_without_end_time_database(self):
        with self.assertRaises(IntegrityError):
            Charge.objects.create(
                project=self.project,
                start_time=timezone.make_aware(
                    datetime(2019, 1, 1, hour=8, minute=0, second=0)),
                closed=True)

    def test_charge_cannot_be_modified_when_closed(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime,
            end_time=start_datetime + timedelta(hours=1),
            closed=True
        ).validate_and_save()

        # Should raise a generic validation error if attempting to
        # save on a closed charge
        with self.assertRaises(ValidationError) as context_manager:
            charge.validate_and_save()

        self.assertValidationMessagePresent(
            context_manager.exception.error_dict,
            field='__all__',
            error_code='cannot_modify_when_closed'
        )

        # But should be able to save the change if it is
        # re-opening the charge
        charge.closed = False
        charge.validate_and_save()
        self.assertEqual(charge.closed, False)

    def test_cannot_delete_project_with_associated_charge(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        Charge(
            project=self.project,
            start_time=start_datetime
        ).validate_and_save()

        with self.assertRaises(ProtectedError):
            self.project.delete()

    def test_charges_are_sorted_by_start_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        Charge(
            project=self.project,
            start_time=start_datetime
        ).validate_and_save()

        earlier_charge = Charge(
            project=self.project,
            start_time=start_datetime - timedelta(hours=1)
        ).validate_and_save()

        later_charge = Charge(
            project=self.project,
            start_time=start_datetime + timedelta(hours=1)
        ).validate_and_save()

        self.assertEqual(Charge.objects.earliest(), earlier_charge)
        self.assertEqual(Charge.objects.latest(), later_charge)
