from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from ProjectTime.project.models import Project


def create_project(**options):
    try:
        project = Project(name=options['name'])
        project.full_clean()
        project.save()
    except ValidationError:
        raise CommandError(
            "Unable to create project due to a validation error.")
    except Exception:
        raise CommandError("Failed to create project.")

    return "Project was successfully created."


class Command(BaseCommand):
    help = "Add a project."

    def add_arguments(self, parser):
        parser.add_argument('name', help='A name for the project.')

    def handle(self, *args, **options):
        success_message = create_project(**options)
        return self.style.SUCCESS(success_message)
