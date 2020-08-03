from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from ProjectTime.project.models import Charge

def close_charge(**options):
    try:
        if options['pk']:
            charge = Charge.objects.get(pk=options['pk'])
        else:
            charge = Charge.objects.filter(closed=False).latest()

        charge.closed = True
        charge.full_clean()
        charge.save()
    except Charge.DoesNotExist:
        if options['pk']:
            raise CommandError(f"No charge with PK `{options['pk']}` found.")
        else:
            raise CommandError("There are no opened charges to close.")
    except ValidationError:
        raise CommandError("Unable to close charge due to a validation error.")
    except Exception:
        raise CommandError("Failed to update charge end time.")

    return "Charge was successfully closed."

class Command(BaseCommand):
    help = "Close a charge."

    def add_arguments(self, parser):
        parser.add_argument(
            '--pk',
            type=int,
            help="The PK of the charge to end (default: latest open)"
        )


    def handle(self, *args, **options):
        success_message = close_charge(**options)
        return self.style.SUCCESS(success_message)
