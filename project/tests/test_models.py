from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, date, timedelta
from ..models import Project, Charge

# Create your tests here.


class ProjectModelTestCase(TestCase):
    def test_project_name_field_display(self):
        name_field = Project._meta.get_field('name')
        self.assertEqual(name_field.verbose_name, 'name')
        self.assertGreater(len(name_field.help_text), 0)

    def test_project_active_field_display(self):
        active_field = Project._meta.get_field('active')
        self.assertEqual(active_field.verbose_name, 'active')
        self.assertGreater(len(active_field.help_text), 0)

    def test_project_can_be_created(self):
        test_name = 'Test'

        project = Project(name=test_name)
        project.full_clean()
        project.save()

        self.assertEqual(project.name, test_name)
        self.assertEqual(project.active, True)

    def test_project_is_string_serializable(self):
        project = Project(name='Test')
        project.full_clean()
        project.save()

        self.assertEqual(str(project), 'Test')

        project.active = False
        project.full_clean()
        project.save()

        self.assertEqual(str(project), 'Test (Inactive)')

    def test_project_name_must_not_exceed_255_characters(self):
        project = Project(name=''.zfill(256))

        with self.assertRaises(ValidationError) as cm:
            project.full_clean()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['name']), 1)
        self.assertEqual(error_dict['name'][0].code, 'max_length')

    def test_project_name_must_not_exceed_255_characters__db(self):
        with self.assertRaises(DataError):
            Project.objects.create(name=''.zfill(256))

    def test_project_name_must_be_unique(self):
        test_name = 'Test'

        project1 = Project(name=test_name)
        project1.full_clean()
        project1.save()

        with self.assertRaises(ValidationError) as cm:
            project2 = Project(name=test_name)
            project2.full_clean()
            project2.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['name']), 1)
        self.assertEqual(error_dict['name'][0].code, 'unique')

    def test_project_name_must_be_unique__db(self):
        test_name = 'Test'

        Project.objects.create(name=test_name)

        with self.assertRaises(IntegrityError):
            Project.objects.create(name=test_name)

    def test_project_active_is_not_required(self):
        active_field = Project._meta.get_field('active')
        self.assertEqual(active_field.blank, True)

    def test_project_active_is_true_by_default(self):
        active_field = Project._meta.get_field('active')
        self.assertEqual(active_field.default, True)

    def test_cannot_modify_project_when_inactive(self):
        project = Project(name='Test', active=False)
        project.full_clean()
        project.save()

        # Should raise a generic validation error if attempting to
        # save on a inactive project
        with self.assertRaises(ValidationError) as cm:
            project.full_clean()
            project.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['__all__']), 1)
        self.assertEqual(error_dict['__all__'][0].code,
                         'cannot_modify_when_inactive')

        # But should be able to save the change if it is
        # re-opening the project
        project.active = True
        project.full_clean()
        project.save()
        self.assertEqual(project.active, True)


class ChargeModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = Project(name='Test')
        cls.project.full_clean()
        cls.project.save()

    def test_charge_project_field_display(self):
        project_field = Charge._meta.get_field('project')
        self.assertEqual(project_field.verbose_name, 'project')
        self.assertGreater(len(project_field.help_text), 0)

    def test_charge_start_time_field_display(self):
        start_time_field = Charge._meta.get_field('start_time')
        self.assertEqual(start_time_field.verbose_name, 'start time')
        self.assertGreater(len(start_time_field.help_text), 0)

    def test_charge_end_time_field_display(self):
        end_time_field = Charge._meta.get_field('end_time')
        self.assertEqual(end_time_field.verbose_name, 'end time')
        self.assertGreater(len(end_time_field.help_text), 0)

    def test_charge_closed_field_display(self):
        closed_field = Charge._meta.get_field('closed')
        self.assertEqual(closed_field.verbose_name, 'closed')
        self.assertGreater(len(closed_field.help_text), 0)

    def test_charge_can_be_created_today(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        timedelta_zero = timedelta()

        charge = Charge(
            project=self.project,
            start_time=today
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.project, self.project)
        self.assertEqual(charge.start_time, today)
        self.assertEqual(charge.end_time, None)
        self.assertEqual(charge.time_charged, timedelta_zero)
        self.assertEqual(charge.closed, False)

    def test_charge_end_time_is_not_required(self):
        end_time_field = Charge._meta.get_field('end_time')
        self.assertTrue(end_time_field.blank)

    def test_charge_end_time_is_nullable(self):
        end_time_field = Charge._meta.get_field('end_time')
        self.assertTrue(end_time_field.null)

    def test_charge_closed_is_not_required(self):
        closed_field = Charge._meta.get_field('closed')
        self.assertTrue(closed_field.blank)

    def test_charge_closed_is_not_nullable(self):
        closed_field = Charge._meta.get_field('closed')
        self.assertFalse(closed_field.null)

    def test_charge_closed_is_false_by_default(self):
        closed_field = Charge._meta.get_field('closed')
        self.assertFalse(closed_field.default)

    def test_cannot_create_charge_with_end_time_before_start_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        # Should raise a keyed validation error
        with self.assertRaises(ValidationError) as cm:
            charge = Charge(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1)
            )
            charge.full_clean()
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['end_time']), 1)
        self.assertEqual(error_dict['end_time'][0].code,
                         'end_time_must_be_on_or_after_start_time')

        # Should raise a generic validation error if the end time field
        # is excluded
        with self.assertRaises(ValidationError) as cm:
            charge = Charge(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1)
            )
            charge.full_clean(exclude=('end_time',))
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['__all__']), 1)
        self.assertEqual(error_dict['__all__'][0].code,
                         'end_time_must_be_on_or_after_start_time')

    def test_cannot_create_charge_with_end_time_before_start_time__db(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        with self.assertRaises(IntegrityError):
            Charge.objects.create(
                project=self.project,
                start_time=start_datetime,
                end_time=start_datetime - timedelta(minutes=1)
            )

    def test_cannot_close_charge_without_end_time(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        # Should raise a keyed validation error
        with self.assertRaises(ValidationError) as cm:
            charge = Charge(
                project=self.project,
                start_time=start_datetime,
                closed=True
            )
            charge.full_clean()
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['closed']), 1)
        self.assertEqual(error_dict['closed'][0].code,
                         'cannot_close_without_end_time')

        # Should raise a generic validation error if the end time field
        # is excluded
        with self.assertRaises(ValidationError) as cm:
            charge = Charge(
                project=self.project,
                start_time=start_datetime,
                closed=True
            )
            charge.full_clean(exclude=('closed',))
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['__all__']), 1)
        self.assertEqual(error_dict['__all__'][0].code,
                         'cannot_close_without_end_time')

    def test_cannot_modify_charge_when_closed(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime,
            end_time=start_datetime + timedelta(hours=1),
            closed=True
        )

        charge.full_clean()
        charge.save()

        # Should raise a generic validation error if attempting to
        # save on a closed charge
        with self.assertRaises(ValidationError) as cm:
            charge.full_clean()
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['__all__']), 1)
        self.assertEqual(error_dict['__all__'][0].code,
                         'cannot_modify_when_closed')

        # But should be able to save the change if it is
        # re-opening the charge
        charge.closed = False
        charge.full_clean()
        charge.save()
        self.assertEqual(charge.closed, False)

    def test_cannot_delete_project_with_associated_charge(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime
        )
        charge.full_clean()
        charge.save()

        with self.assertRaises(ProtectedError):
            self.project.delete()

    def test_time_charged_is_correct(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))
        timedelta_zero = timedelta()
        added_time = timedelta(minutes=30)

        charge = Charge(
            project=self.project,
            start_time=start_datetime
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.time_charged, timedelta_zero)

        charge.end_time = start_datetime + added_time
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.time_charged, added_time)

    def test_charge_is_string_serializable(self):
        start_datetime = timezone.make_aware(
            datetime(2019, 1, 1, hour=8, minute=0, second=0))

        charge = Charge(
            project=self.project,
            start_time=start_datetime
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test, 2019-01-01 08:00:00+00:00 - __:__:__ (0:00:00 minutes) [Open]')

        charge.end_time = start_datetime + timedelta(minutes=30)
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test, 2019-01-01 08:00:00+00:00 - 2019-01-01 08:30:00+00:00 (0:30:00 minutes) [Open]')

        charge.end_time = start_datetime + timedelta(hours=1)
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test, 2019-01-01 08:00:00+00:00 - 2019-01-01 09:00:00+00:00 (1:00:00 hours) [Open]')

        charge.end_time = start_datetime + timedelta(hours=1, minutes=15)
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test, 2019-01-01 08:00:00+00:00 - 2019-01-01 09:15:00+00:00 (1:15:00 hours) [Open]')

        charge.closed = True
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test, 2019-01-01 08:00:00+00:00 - 2019-01-01 09:15:00+00:00 (1:15:00 hours) [Closed]')

    def test_charges_are_ordered_by_charge_date_and_start_time(self):
        ordered_charges = self.get_ordered_test_charge_list()

        self.assertQuerysetEqual(Charge.objects.all(),
                                 ordered_charges,
                                 transform=lambda charge: charge)

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

        self.create_test_charges(charge_timedeltas)
        self.assertQuerysetEqual(
            Charge.objects.annotate_time_charged(),
            charge_timedeltas,
            transform=lambda charge: charge.db__time_charged
        )

    def test_get_charge_list_aggregate_time(self):
        charge_timedeltas = (
            timedelta(seconds=30),
            timedelta(minutes=15),
            timedelta(hours=1),
        )

        self.create_test_charges(charge_timedeltas)
        self.assertEqual(Charge.objects.aggregate_time_charged(),
                         sum(charge_timedeltas, timedelta()))

    ### Helper Methods ###

    def create_test_charges(self, charge_timedeltas):
        next_charge_start_datetime = timezone.make_aware(datetime(
            2019, 1, 1, hour=0, minute=0, second=0))
        charges = []

        for charge_time in charge_timedeltas:
            charge_end_datetime = next_charge_start_datetime + charge_time
            charge = Charge(
                project=self.project,
                start_time=next_charge_start_datetime,
                end_time=charge_end_datetime
            )
            charge.full_clean()
            charge.save()
            charges.append(charge)

            next_charge_start_datetime = charge_end_datetime

    def get_ordered_test_charge_list(self):
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
            charge = Charge(
                project=self.project,
                start_time=entry
            )
            charge.full_clean()
            charge.save()

            ordered_charges.append(charge)

        return ordered_charges
