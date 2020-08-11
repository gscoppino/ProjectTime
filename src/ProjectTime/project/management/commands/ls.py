""" Exposes management commands for listing projects and charges.
"""

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.utils import timezone
from django.utils.formats import localize

from ProjectTime.project.models import Charge, Project


def _localize_datetime(pdvalue):
    if pdvalue is pd.NaT:
        return None

    return localize(timezone.localtime(pdvalue.to_pydatetime()), use_l10n=settings.USE_L10N)


def _localize_timedelta(pdvalue):
    if pdvalue is pd.NaT:
        return None

    return localize(pdvalue.to_pytimedelta(), use_l10n=settings.USE_L10N)


def get_projects_dataframe(**options):
    try:
        projects = Project.objects.annotate_latest_charge()

        if not options['all']:
            projects = projects.filter(active=True)

        df = projects.to_pandas(
            'pk',
            'name',
            'active',
            'db__latest_charge',
        ).astype({
            "db__latest_charge": 'datetime64[ns, UTC]'
        })
    except Exception:
        raise CommandError("Failed to retrieve the project list.")

    if df.empty:
        return df

    df.update(df.db__latest_charge.apply(_localize_datetime))

    return df.set_index('pk').sort_index().rename(columns={
        "name": "Name",
        "active": "Active",
        "db__latest_charge": "Latest Charge"
    })


def get_open_charges_dataframe(**options):
    try:
        charges = (Charge.objects
                   .select_related('project')
                   .annotate(project_name=F('project__name'))
                   .annotate_time_charged())

        if options['project']:
            charges = charges.filter(project__name=options['project'])

        if not options['all']:
            charges = charges.filter(closed=False)

        df = charges.to_pandas(
            'pk',
            'project__name',
            'start_time',
            'end_time',
            'db__time_charged',
            'closed',
        ).astype({
            "start_time": 'datetime64[ns, UTC]',
            "end_time": 'datetime64[ns, UTC]',
            "db__time_charged": 'timedelta64[ns]'
        })

    except Exception:
        raise CommandError("Failed to retrieve the charge list.")

    if df.empty:
        return df

    df.update(df.start_time.apply(_localize_datetime))
    df.update(df.end_time.apply(_localize_datetime))
    df.update(df.db__time_charged.apply(_localize_timedelta))

    return df.set_index('pk').sort_index().rename(columns={
        'project__name': 'Project',
        'start_time': 'Start Time',
        'end_time': 'End Time',
        'db__time_charged': 'Time Charged',
        'closed': 'Closed'
    })


class Command(BaseCommand):
    """ Management command for listing projects and charges.
    """
    help = "List records."

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(required=True, dest="command")

        projects_parser = subparsers.add_parser("projects")
        projects_parser.add_argument(
            '-a', '--all', action="store_true", help="List inactive projects as well."
        )

        charges_parser = subparsers.add_parser("charges")
        charges_parser.add_argument(
            '-a', '--all', action="store_true", help="List closed charges as well."
        )
        charges_parser.add_argument(
            '-p', '--project', help="Filter results to a specific project."
        )

    def handle(self, *args, **options):
        timezone.activate(settings.PROJECT_TIME_CLI_TIMEZONE)

        pd.set_option("display.width", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)

        if options['command'] == "projects":
            return get_projects_dataframe(**options).to_markdown()

        if options['command'] == "charges":
            return get_open_charges_dataframe(**options).to_markdown()

        return CommandError("Unrecognized record type.")
