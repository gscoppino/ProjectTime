from datetime import timedelta

import pandas as pd
from django.test import TestCase
from django.utils import timezone

from ProjectTime.project.models import Charge, Project
from ProjectTime.project.utils import reporting as report_helpers

from .utils.charge import ChargeFactory
from .utils.general import get_start_of_today


class ReportingHelpersTestCase(TestCase):
    def test_visualization_creation_whitebox(self):
        project_a = Project(name='Project A').validate_and_save()
        project_b = Project(name='Project B').validate_and_save()

        # Create some test charges in the current month

        project_a_current_charges = [
            timedelta(hours=4),
            timedelta(hours=4),
        ]

        project_b_current_charges = [
            timedelta(hours=4),
            timedelta(hours=4),
        ]

        for charge in project_a_current_charges:
            ChargeFactory.today(
                project=project_a,
                charge_time=charge
            ).validate_and_save()

        for charge in project_b_current_charges:
            ChargeFactory.today(
                project=project_b,
                charge_time=charge
            ).validate_and_save()

        # Create some unclosed charges in the current month
        Charge(
            project=project_a,
            start_time=get_start_of_today()
        ).validate_and_save()

        Charge(
            project=project_b,
            start_time=get_start_of_today()
        ).validate_and_save()

        # Create charges in a past month

        ChargeFactory.past_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        ChargeFactory.past_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        # Create charges in a future month

        ChargeFactory.future_month(
            project=project_a,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        ChargeFactory.future_month(
            project=project_b,
            charge_time=timedelta(hours=1)
        ).validate_and_save()

        # Should return data on all projects

        dataframe = report_helpers.get_monthly_summary_series(timezone.localtime())

        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(len(dataframe), 2)

        self.assertIsInstance(dataframe['charge'], pd.Series)
        self.assertIsInstance(dataframe['value'], pd.Series)
        self.assertIsInstance(dataframe['angle'], pd.Series)
        self.assertIsInstance(dataframe['color'], pd.Series)

        project_a_dataframe = dataframe[dataframe.charge == project_a.name]
        project_b_dataframe = dataframe[dataframe.charge == project_b.name]

        self.assertFalse(project_a_dataframe.empty)
        self.assertFalse(project_b_dataframe.empty)

        self.assertEqual(project_a_dataframe.iloc[0].value, 8.0)
        self.assertEqual(project_b_dataframe.iloc[0].value, 8.0)

        self.assertIsInstance(project_a_dataframe.iloc[0].angle, float)
        self.assertIsInstance(project_b_dataframe.iloc[0].angle, float)

        self.assertIsInstance(project_a_dataframe.iloc[0].color, str)
        self.assertIsInstance(project_b_dataframe.iloc[0].color, str)

        div, chart = report_helpers.get_monthly_summary_chart_components(dataframe)
        self.assertGreater(len(div), 0)
        self.assertGreater(len(chart), 0)

        # Should return data on only the requested projects

        dataframe = report_helpers.get_monthly_summary_series(timezone.localtime(),
                                                    project_ids=[project_a.pk])

        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(len(dataframe), 1)

        self.assertIsInstance(dataframe['charge'], pd.Series)
        self.assertIsInstance(dataframe['value'], pd.Series)
        self.assertIsInstance(dataframe['angle'], pd.Series)
        self.assertIsInstance(dataframe['color'], pd.Series)

        self.assertEqual(dataframe.iloc[0].charge, project_a.name)
        self.assertEqual(dataframe.iloc[0].value, 8.0)
        self.assertIsInstance(dataframe.iloc[0].angle, float)
        self.assertIsInstance(dataframe.iloc[0].color, str)

        div, chart = report_helpers.get_monthly_summary_chart_components(dataframe)
        self.assertGreater(len(div), 0)
        self.assertGreater(len(chart), 0)
