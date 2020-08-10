from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ProjectTime.project.models import Charge, Project

from .utils.general import validate_and_save


class ProjectQuerySetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = validate_and_save(Project(name='Test'))

    def test_project_has_latest_charge_annotated(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        validate_and_save(Charge(
            project=self.project,
            start_time=yesterday,
            end_time=today))

        validate_and_save(Charge(
            project=self.project,
            start_time=today,
            end_time=tomorrow
        ))

        annotated_project = (Project.objects.annotate_latest_charge()
                             .get(pk=self.project.pk))

        self.assertEqual(annotated_project.db__latest_charge, tomorrow)


class ChargeQuerySetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = validate_and_save(Project(name='Test'))

    def test_charge_has_time_charged_annotated(self):
        start_of_today = timezone.now().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)

        charge = validate_and_save(Charge(
            project=self.project,
            start_time=start_of_today.replace(hour=9),
            end_time=start_of_today.replace(hour=17)
        ))

        annotated_charge = (Charge.objects.annotate_time_charged()
                            .get(pk=charge.pk))

        self.assertEqual(annotated_charge.db__time_charged, timedelta(hours=8))

    def test_get_aggregated_time_charged(self):
        start_of_today = timezone.now().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)

        validate_and_save(Charge(
            project=self.project,
            start_time=start_of_today.replace(hour=8),
            end_time=start_of_today.replace(hour=9)
        ))

        validate_and_save(Charge(
            project=self.project,
            start_time=start_of_today.replace(hour=9),
            end_time=start_of_today.replace(hour=17)
        ))

        total_time_charged = Charge.objects.aggregate_time_charged()
        self.assertEqual(total_time_charged, timedelta(hours=9))
