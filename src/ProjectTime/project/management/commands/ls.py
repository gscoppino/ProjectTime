import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.utils import timezone
from django.utils.formats import localize
from ProjectTime.project.models import Project, Charge
from ProjectTime.project.management.utils.timezone import activate_timezone_for_cli

def _localize_datetime(value):
    if value is None:
        return None

    return localize(timezone.localtime(value), use_l10n=settings.USE_L10N)

def _localize_timedelta(value):
    if value is None:
        return None

    return localize(value, use_l10n=settings.USE_L10N)

def get_projects_dataframe(**options):
    try:
        projects = Project.objects.annotate_latest_charge().values_list(
            'pk',
            'name',
            'active',
            'db__latest_charge',
            named=True
        )
    except Exception:
        raise CommandError("Failed to retrieve the project list.")

    projects = [project._replace(
        db__latest_charge=_localize_datetime(project.db__latest_charge)
    ) for project in projects]

    df = pd.DataFrame(
        projects, columns=('PK', 'Name', 'Active', 'Latest Charge')
    ).set_index('PK').sort_index()

    return df

def get_open_charges_dataframe(**options):
    try:
        charges = (
            Charge.objects
                .filter(closed=False)
                .select_related('project')
                .annotate(project_name=F('project__name'))
                .annotate_time_charged()
                .values_list(
                    'pk',
                    'project__name',
                    'start_time',
                    'end_time',
                    'db__time_charged',
                    'closed',
                    named=True
                )
        )
    except Exception:
        raise CommandError("Failed to retrieve the charge list.")

    charges = [charge._replace(
        start_time=_localize_datetime(charge.start_time),
        end_time=_localize_datetime(charge.end_time),
        db__time_charged=_localize_timedelta(charge.db__time_charged)
    ) for charge in charges]

    df = pd.DataFrame(
        charges, columns=('PK', 'Project', 'Start', 'End', 'Time Charged', 'Closed')
    ).set_index('PK').sort_index()

    return df

class Command(BaseCommand):
    help = "List records."

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(required=True, dest="command")

        subparsers.add_parser("projects")
        subparsers.add_parser("charges")
    
    def handle(self, *args, **options):
        activate_timezone_for_cli()
        pd.set_option("display.width", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.colheader_justify", "left")

        if options['command'] == "projects":
            return str(get_projects_dataframe(**options))
        elif options['command'] == "charges":
            return str(get_open_charges_dataframe(**options))
        else:
            return CommandError("Unrecognized record type.")