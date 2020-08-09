from django.core.management.base import BaseCommand, CommandError
from ProjectTime.project.models import Charge


def delete_charge(**options):
    try:
        if options['pk']:
            charge = Charge.objects.get(pk=options['pk'])
        else:
            charge = Charge.objects.filter(closed=False).latest()

        charge.delete()
    except Charge.DoesNotExist:
        if options['pk']:
            raise CommandError(f"No charge with PK `{options['pk']}` found.")

        raise CommandError("There are no opened charges to delete.")
    except Exception:
        raise CommandError("Failed to delete charge.")

    return "Charge was successfully deleted."


class Command(BaseCommand):
    help = "Delete a charge."

    def add_arguments(self, parser):
        parser.add_argument(
            '--pk',
            type=int,
            help="The PK of the charge to delete (default: latest open)"
        )

    def handle(self, *args, **options):
        success_message = delete_charge(**options)
        return self.style.SUCCESS(success_message)
