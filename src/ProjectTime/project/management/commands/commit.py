from datetime import time, datetime
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ProjectTime.project.models import Charge
from ProjectTime.project.management.utils.timezone import activate_timezone_for_cli


def end_charge(**options):
    try:
        if options['pk']:
            charge = Charge.objects.get(pk=options['pk'])
        else:
            charge = Charge.objects.filter(closed=False).latest()

        charge.end_time = timezone.make_aware(
            datetime.combine(
                timezone.localtime(charge.start_time).date(),
                options['end']
            )
        )
        charge.closed = options['close']
        charge.full_clean()
        charge.save()
    except Charge.DoesNotExist:
        if options['pk']:
            raise CommandError(f"No charge with PK `{options['pk']}` found.")
        else:
            raise CommandError("There are no open charges to end.")
    except ValidationError:
        raise CommandError("Unable to end charge due to a validation error.")
    except Exception:
        raise CommandError("Failed to update charge end time.")

    return "Charge end time was successfully updated."


class Command(BaseCommand):
    help = "Commit an end time for a charge."

    def add_arguments(self, parser):
        parser.add_argument(
            '--pk',
            type=int,
            help="The PK of the charge to end (default: latest open)"
        )
        parser.add_argument(
            '-e', '--end',
            type=time.fromisoformat,
            help='The time to end the charge on, in ISO format (default: now).'
        )
        parser.add_argument(
            '-c', '--close',
            action="store_true",
            help="Close the charge."
        )

    def handle(self, *args, **options):
        activate_timezone_for_cli()
        now = timezone.localtime()

        if not options['end']:
            options['end'] = now.time()

        success_message = end_charge(**options)
        return self.style.SUCCESS(success_message)