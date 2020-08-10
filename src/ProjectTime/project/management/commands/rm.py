from django.core.management.base import BaseCommand, CommandError
from django.db.models.deletion import ProtectedError

from ProjectTime.project.models import Project


def delete_project(**options):
    try:
        project = Project.objects.get(name=options['name'])
        project.delete()
    except Project.DoesNotExist:
        raise CommandError(f"No project with name `{options['name']} found.")
    except ProtectedError:
        raise CommandError(
            "Unable to delete project due to database protection.")
    except Exception:
        raise CommandError("Failed to delete project.")

    return "Project was successfully deleted."


class Command(BaseCommand):
    help = "Delete a project."

    def add_arguments(self, parser):
        parser.add_argument('name', help="The name of the project.")

    def handle(self, *args, **options):
        success_message = delete_project(**options)
        return self.style.SUCCESS(success_message)
