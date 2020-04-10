from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date, timedelta
from ..models import Project, Charge
from ..querysets import ProjectQuerySet, ChargeQuerySet
from .utils.general import validate_and_save
from .utils.charge import create_test_charges

# Create your tests here.


def get_model_field(model_class, field_name):
    return model_class._meta.get_field(field_name)


class ModelTestCase(TestCase):
    def assertFailsDatabaseConstraint(self, model_class, **kwargs):
        with self.assertRaises(IntegrityError):
            model_class.objects.create(**kwargs)

    def assertFailsDatabaseMaxLengthRestriction(self, model_class, **kwargs):
        with self.assertRaises(DataError):
            model_class.objects.create(**kwargs)

    def assertValidationErrorOnSave(self, instance=None, field=None, error_code=None, clean_kwargs={}, save_kwargs={}):
        with self.assertRaises(ValidationError) as cm:
            validate_and_save(instance,
                              clean_kwargs=clean_kwargs,
                              save_kwargs=save_kwargs)

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict[field]), 1)
        self.assertEqual(error_dict[field][0].code, error_code)


class ProjectModelTestCase(ModelTestCase):
    def test_project_has_custom_queryset_manager(self):
        self.assertQuerysetEqual(Project.objects.get_queryset(),
                                 ProjectQuerySet(model=Project))

    def test_project_name_field_display(self):
        field = get_model_field(Project, 'name')
        self.assertEqual(field.verbose_name, 'name')
        self.assertGreater(len(field.help_text), 0)

    def test_project_active_field_display(self):
        field = get_model_field(Project, 'active')
        self.assertEqual(field.verbose_name, 'active')
        self.assertGreater(len(field.help_text), 0)

    def test_project_can_be_created(self):
        test_name = 'Test'
        project = validate_and_save(Project(name=test_name))

        self.assertEqual(project.name, test_name)
        self.assertEqual(project.active, True)

    def test_project_is_string_serializable(self):
        project = validate_and_save(Project(name='Test'))

        self.assertEqual(str(project), 'Test')

        project.active = False
        validate_and_save(project)

        self.assertEqual(str(project), 'Test (Inactive)')

    def test_project_name_must_not_exceed_255_characters(self):
        self.assertValidationErrorOnSave(instance=Project(name=''.zfill(256)),
                                         field='name',
                                         error_code='max_length')

    def test_project_name_must_not_exceed_255_characters__db(self):
        self.assertFailsDatabaseMaxLengthRestriction(
            Project,
            name=''.zfill(256))

    def test_project_name_must_be_unique(self):
        test_name = 'Test'

        validate_and_save(Project(name=test_name))
        self.assertValidationErrorOnSave(instance=Project(name=test_name),
                                         field='name',
                                         error_code='unique')

    def test_project_name_must_be_unique__db(self):
        test_name = 'Test'

        validate_and_save(Project(name=test_name))
        self.assertFailsDatabaseConstraint(Project, name=test_name)

    def test_project_active_is_not_required(self):
        active_field = get_model_field(Project, 'active')
        self.assertEqual(active_field.blank, True)

    def test_project_active_is_true_by_default(self):
        active_field = get_model_field(Project, 'active')
        self.assertEqual(active_field.default, True)

    def test_cannot_modify_project_when_inactive(self):
        project = validate_and_save(Project(name='Test', active=False))

        # Should raise a generic validation error if attempting to
        # save on a inactive project
        self.assertValidationErrorOnSave(instance=project,
                                         field='__all__',
                                         error_code='cannot_modify_when_inactive')

        # But should be able to save the change if it is
        # re-opening the project
        project.active = True
        validate_and_save(project)
        self.assertEqual(project.active, True)


class ChargeModelTestCase(ModelTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = validate_and_save(Project(name='Test'))

    def test_charge_has_custom_queryset_manager(self):
        self.assertQuerysetEqual(Charge.objects.get_queryset(),
                                 ChargeQuerySet(model=Charge))

    def test_charge_project_field_display(self):
        field = get_model_field(Charge, 'project')
        self.assertEqual(field.verbose_name, 'project')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_start_time_field_display(self):
        field = get_model_field(Charge, 'start_time')
        self.assertEqual(field.verbose_name, 'start time')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_end_time_field_display(self):
        field = get_model_field(Charge, 'end_time')
        self.assertEqual(field.verbose_name, 'end time')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_closed_field_display(self):
        field = get_model_field(Charge, 'closed')
        self.assertEqual(field.verbose_name, 'closed')
        self.assertGreater(len(field.help_text), 0)

    def test_charge_can_be_created_today(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        timedelta_zero = timedelta()

        charge = validate_and_save(Charge(
            project=self.project,
            start_time=today
        ))

        self.assertEqual(charge.project, self.project)
        self.assertEqual(charge.start_time, today)
        self.assertEqual(charge.end_time, None)
        self.assertEqual(charge.time_charged, timedelta_zero)
        self.assertEqual(charge.closed, False)

    def test_charge_end_time_is_not_required(self):
        end_time_field = get_model_field(Charge, 'end_time')
        self.assertTrue(end_time_field.blank)

    def test_charge_end_time_is_nullable(self):
        end_time_field = get_model_field(Charge, 'end_time')
        self.assertTrue(end_time_field.null)

    def test_charge_closed_is_not_required(self):
        closed_field = get_model_field(Charge, 'closed')
        self.assertTrue(closed_field.blank)

    def test_charge_closed_is_not_nullable(self):
        closed_field = get_model_field(Charge, 'closed')
        self.assertFalse(closed_field.null)

    def test_charge_closed_is_false_by_default(self):
        closed_field = get_model_field(Charge, 'closed')
        self.assertFalse(closed_field.default)

    def test_cannot_save_with_inactive_project(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        inactive_project = validate_and_save(Project(
            name='Test 2',
            active=False))

        # Should raise a keyed validation error
        self.assertValidationErrorOnSave(
            instance=Charge(
                project=inactive_project,
                start_time=start_datetime,
                end_time=start_datetime + timedelta(hours=1)
            ),
            field='project',
            error_code='project_must_be_active')

    def test_cannot_create_charge_with_end_time_before_start_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        # Should raise a keyed validation error
        self.assertValidationErrorOnSave(
            instance=Charge(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1)
            ),
            field='end_time',
            error_code='end_time_must_be_on_or_after_start_time')

        # Should raise a generic validation error if the end time field
        # is excluded
        self.assertValidationErrorOnSave(
            instance=Charge(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1)
            ),
            clean_kwargs={'exclude': ('end_time',)},
            field='__all__',
            error_code='end_time_must_be_on_or_after_start_time')

    def test_cannot_create_charge_with_end_time_before_start_time__db(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        self.assertFailsDatabaseConstraint(
            Charge,
            project=self.project,
            start_time=start_datetime,
            end_time=start_datetime - timedelta(minutes=1))

    def test_cannot_close_charge_without_end_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        # Should raise a keyed validation error
        self.assertValidationErrorOnSave(
            instance=Charge(
                project=self.project,
                start_time=start_datetime,
                closed=True
            ),
            field='closed',
            error_code='cannot_close_without_end_time')

        # Should raise a generic validation error if the end time field
        # is excluded
        self.assertValidationErrorOnSave(
            instance=Charge(
                project=self.project,
                start_time=start_datetime,
                closed=True
            ),
            clean_kwargs={'exclude': ('closed',)},
            field='__all__',
            error_code='cannot_close_without_end_time')

    def test_cannot_close_without_end_time__db(self):
        self.assertFailsDatabaseConstraint(
            Charge,
            project=self.project,
            start_time=timezone.make_aware(
                datetime(2019, 1, 1, hour=8, minute=0, second=0)),
            closed=True
        )

    def test_cannot_modify_charge_when_closed(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = validate_and_save(Charge(
            project=self.project,
            start_time=start_datetime,
            end_time=start_datetime + timedelta(hours=1),
            closed=True
        ))

        # Should raise a generic validation error if attempting to
        # save on a closed charge
        self.assertValidationErrorOnSave(
            instance=charge,
            field='__all__',
            error_code='cannot_modify_when_closed')

        # But should be able to save the change if it is
        # re-opening the charge
        charge.closed = False
        validate_and_save(charge)
        self.assertEqual(charge.closed, False)

    def test_cannot_delete_project_with_associated_charge(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        validate_and_save(Charge(
            project=self.project,
            start_time=start_datetime
        ))

        with self.assertRaises(ProtectedError):
            self.project.delete()

    def test_time_charged_is_correct(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))
        timedelta_zero = timedelta()
        added_time = timedelta(minutes=30)

        charge = validate_and_save(Charge(
            project=self.project,
            start_time=start_datetime
        ))

        self.assertEqual(charge.time_charged, timedelta_zero)

        charge.end_time = start_datetime + added_time
        validate_and_save(charge)

        self.assertEqual(charge.time_charged, added_time)

    def test_charge_is_string_serializable(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = validate_and_save(Charge(
            project=self.project,
            start_time=start_datetime
        ))

        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - __:__:__ (0:00:00 minutes) [Open]')

        charge.end_time = start_datetime + timedelta(minutes=30)
        validate_and_save(charge)

        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 8:30 a.m. (0:30:00 minutes) [Open]')

        charge.end_time = start_datetime + timedelta(hours=1)
        validate_and_save(charge)

        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9 a.m. (1:00:00 hours) [Open]')

        charge.end_time = start_datetime + timedelta(hours=1, minutes=15)
        validate_and_save(charge)

        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9:15 a.m. (1:15:00 hours) [Open]')

        charge.closed = True
        validate_and_save(charge)

        self.assertEqual(
            str(charge), 'Test, Jan. 1, 2019, 8 a.m. - Jan. 1, 2019, 9:15 a.m. (1:15:00 hours) [Closed]')

    def test_get_earliest_charge(self):
        ordered_charges = self.get_ordered_test_charge_list()
        self.assertEqual(Charge.objects.earliest(), ordered_charges[0])

    def test_get_latest_charge(self):
        ordered_charges = self.get_ordered_test_charge_list()
        self.assertEqual(Charge.objects.latest(), ordered_charges[-1])

    def test_get_annotated_charge_list(self):
        charge_timedeltas = (
            timedelta(seconds=30),
            timedelta(minutes=15),
            timedelta(hours=1),
        )

        create_test_charges(
            self.project,
            timezone.make_aware(datetime(
                2019, 1, 1, hour=0, minute=0, second=0
            )),
            charge_timedeltas)

        self.assertQuerysetEqual(
            Charge.objects.annotate_time_charged().order_by('start_time'),
            charge_timedeltas,
            transform=lambda charge: charge.db__time_charged
        )

    def test_get_charge_list_aggregate_time(self):
        charge_timedeltas = (
            timedelta(seconds=30),
            timedelta(minutes=15),
            timedelta(hours=1),
        )

        create_test_charges(
            self.project,
            timezone.make_aware(datetime(
                2019, 1, 1, hour=0, minute=0, second=0
            )),
            charge_timedeltas)

        self.assertEqual(Charge.objects.aggregate_time_charged(),
                         sum(charge_timedeltas, timedelta()))

    ### Helper Methods ###

    @classmethod
    def get_ordered_test_charge_list(cls):
        baseline = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))
        plus_one_hour = baseline + timedelta(hours=1)
        minus_one_hour = baseline - timedelta(hours=1)
        plus_one_day = baseline + timedelta(days=1)
        minus_one_day = baseline - timedelta(days=1)

        ordered_datetimes = (minus_one_day, minus_one_hour,
                             baseline, plus_one_hour, plus_one_day,)
        ordered_charges = []

        for entry in ordered_datetimes:
            ordered_charges.append(validate_and_save(Charge(
                project=cls.project,
                start_time=entry
            )))

        return ordered_charges
