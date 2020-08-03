from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from ProjectTime.project.models import Project

def activate_project(**options):
    try:
        project = Project.objects.get(name=options['name'])
        if project.active == True:
            return "Project is already active."

        project.active = True
        project.full_clean()
        project.save()
    except Project.DoesNotExist:
        raise CommandError(f"No project with name `{options['name']}` found.")
    except ValidationError as e:
        raise CommandError("Unable to activate project due to a validation error.")
    except Exception:
        raise CommandError("Failed to activate project.")

    return "Project was successfully activated."

class Command(BaseCommand):
    help = "Mark a project as active."

    def add_arguments(self, parser):
        parser.add_argument('name', help='The name of the project')

    def handle(self, *args, **options):
        success_message = activate_project(**options)
        return self.style.SUCCESS(success_message)