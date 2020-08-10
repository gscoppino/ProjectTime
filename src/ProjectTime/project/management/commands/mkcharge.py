from datetime import date, datetime, time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ProjectTime.project.models import Charge, Project


def create_charge(**options):
    try:
        project = Project.objects.get(name=options['name'])
        start_time = timezone.make_aware(
            datetime.combine(options['date'], options['start'])
        )
        if options['end']:
            end_time = timezone.make_aware(
                datetime.combine(options['date'], options['end'])
            )
        else:
            end_time = None

        charge = Charge(
            project=project,
            start_time=start_time,
            end_time=end_time,
            closed=options['close']
        )

        charge.full_clean()
        charge.save()
    except ValidationError:
        raise CommandError(
            "Unable to create charge due to a validation error.")
    except Exception:
        raise CommandError("Failed to create charge.")

    return "Charge was successfully created."


class Command(BaseCommand):
    help = "Add a charge."

    def add_arguments(self, parser):
        parser.add_argument('name', help='The name of the project to charge.')
        parser.add_argument(
            '-d', '--date',
            type=date.fromisoformat,
            help='The date to charge on, in ISO format (default: today).'
        )
        parser.add_argument(
            '-s', '--start',
            type=time.fromisoformat,
            help='The time to start the charge on, in ISO format (default: now).'
        )

        parser.add_argument(
            '-e', '--end',
            type=time.fromisoformat,
            help='The time to end the charge on, in ISO format.'
        )
        parser.add_argument(
            '-c', '--close',
            action='store_true',
            help='Mark the charge as closed'
        )

    def handle(self, *args, **options):
        timezone.activate(settings.PROJECT_TIME_CLI_TIMEZONE)
        now = timezone.localtime()

        if not options['date']:
            options['date'] = now.date()
        if not options['start']:
            options['start'] = now.time()

        success_message = create_charge(**options)
        return self.style.SUCCESS(success_message)
