# pylint: disable=invalid-name
""" Defines a management command for marking projects as inactive.
"""

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from ProjectTime.project.models import Project


def deactivate_project(**options):
    try:
        project = Project.objects.get(name=options['name'])
        if not project.active:
            return "Project is already inactive."

        project.active = False
        project.full_clean()
        project.save()
    except Project.DoesNotExist:  # pylint: disable=no-member
        raise CommandError(f"No project with name `{options['name']}` found.")
    except ValidationError:
        raise CommandError(
            "Unable to deactivate project due to a validation error.")
    except Exception:
        raise CommandError("Failed to deactivate project.")

    return "Project was successfully deactivated."


class Command(BaseCommand):
    """ Management command for marking projects as inactive.
    """
    help = "Mark a project as inactive."

    def add_arguments(self, parser):
        parser.add_argument('name', help='The name of the project')

    def handle(self, *args, **options):
        success_message = deactivate_project(**options)
        return self.style.SUCCESS(success_message)
