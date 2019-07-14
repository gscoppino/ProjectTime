from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError
from django.test import TestCase
from datetime import datetime, timedelta
from ..models import Project, Charge

# Create your tests here.


class ProjectTestCase(TestCase):

    def test_project_can_be_created(self):
        test_name = 'Test'

        project = Project(name=test_name)
        project.full_clean()
        project.save()

        self.assertEqual(project.name, test_name)

    def test_project_is_string_serializable(self):
        test_name = 'Test'

        project = Project(name=test_name)
        project.full_clean()
        project.save()

        self.assertEqual(str(project), test_name)

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


class ChargeTestCase(TestCase):
    def test_charge_can_be_created_correctly_today(self):
        today = datetime.today()
        todays_date = today.date()
        todays_current_time = today.time()
        timedelta_zero = timedelta()

        project = Project(name='Test')
        project.full_clean()
        project.save()

        charge = Charge(
            project=project,
            date=todays_date,
            start_time=todays_current_time
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.project, project)
        self.assertEqual(charge.date, todays_date)
        self.assertEqual(charge.start_time, todays_current_time)
        self.assertEqual(charge.end_time, None)
        self.assertEqual(charge.time_charged, timedelta_zero)

    def test_cannot_create_charge_with_end_time_before_start_time(self):
        start_datetime = datetime(2019, 1, 1, hour=8, minute=0, second=0)

        project = Project(name='Test')
        project.full_clean()
        project.save()

        with self.assertRaises(ValidationError) as cm:
            charge = Charge(
                project=project,
                date=start_datetime.date(),
                start_time=start_datetime.time(),
                end_time=(start_datetime - timedelta(minutes=1)).time()
            )
            charge.full_clean()
            charge.save()

        error_dict = cm.exception.error_dict
        self.assertEqual(len(error_dict.keys()), 1)
        self.assertEqual(len(error_dict['end_time']), 1)
        self.assertEqual(error_dict['end_time'][0].code,
                         'end_time_must_be_on_or_after_start_time')

    def test_cannot_create_charge_with_end_time_before_start_time__db(self):
        start_datetime = datetime(2019, 1, 1, hour=8, minute=0, second=0)

        project = Project.objects.create(name='Test')

        with self.assertRaises(IntegrityError):
            Charge.objects.create(
                project=project,
                date=start_datetime.date(),
                start_time=start_datetime.time(),
                end_time=(start_datetime - timedelta(minutes=1)).time()
            )

    def test_time_charged_is_correct(self):
        start_datetime = datetime(2019, 1, 1, hour=8, minute=0, second=0)
        timedelta_zero = timedelta()
        added_time = timedelta(minutes=30)

        project = Project(name='Test')
        project.full_clean()
        project.save()

        charge = Charge(
            project=project,
            date=start_datetime.date(),
            start_time=start_datetime.time()
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.time_charged, timedelta_zero)

        charge.end_time = (start_datetime + added_time).time()
        charge.full_clean()
        charge.save()

        self.assertEqual(charge.time_charged, added_time)

    def test_charge_is_string_serializable(self):
        start_datetime = datetime(2019, 1, 1, hour=8, minute=0, second=0)

        project = Project(name='Test')
        project.full_clean()
        project.save()

        charge = Charge(
            project=project,
            date=start_datetime.date(),
            start_time=start_datetime.time()
        )
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test on 2019-01-01, 08:00:00 - __:__:__ (0:00:00 minutes)')

        charge.end_time = (start_datetime + timedelta(minutes=30)).time()
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test on 2019-01-01, 08:00:00 - 08:30:00 (0:30:00 minutes)')

        charge.end_time = (start_datetime + timedelta(hours=1)).time()
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test on 2019-01-01, 08:00:00 - 09:00:00 (1:00:00 hours)')

        charge.end_time = (
            start_datetime + timedelta(hours=1, minutes=15)).time()
        charge.full_clean()
        charge.save()

        self.assertEqual(
            str(charge), 'Test on 2019-01-01, 08:00:00 - 09:15:00 (1:15:00 hours)')
