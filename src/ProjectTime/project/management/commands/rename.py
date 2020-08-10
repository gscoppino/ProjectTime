""" Defines a management command for renaming projects.
"""

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from ProjectTime.project.models import Project


def rename_project(**options):
    try:
        project = Project.objects.get(name=options['current_name'])
        if project.name == options['new_name']:
            return "The new name is the same as the current name."

        project.name = options['new_name']
        project.full_clean()
        project.save()
    except Project.DoesNotExist:  # pylint: disable=no-member
        raise CommandError(f"No project with name `{options['name']}` found.")
    except ValidationError:
        raise CommandError(
            "Unable to rename project due to a validation error.")
    except Exception:
        raise CommandError("Failed to rename project.")

    return "Project was successfully renamed."


class Command(BaseCommand):
    """ Management command for renaming projects.
    """
    help = "Rename a project."

    def add_arguments(self, parser):
        parser.add_argument(
            'current_name', help='The current name of the project.')
        parser.add_argument('new_name', help='The new name for the project.')

    def handle(self, *args, **options):
        success_message = rename_project(**options)
        return self.style.SUCCESS(success_message)
