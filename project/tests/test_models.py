from django.db import IntegrityError
from django.test import TestCase
from ..models import Project, Charge

# Create your tests here.


class ProjectTestCase(TestCase):
    def test_project_name_must_be_unique(self):
        test_name = 'Test'

        Project.objects.create(name=test_name)
        with self.assertRaisesRegex(IntegrityError, 'UNIQUE constraint failed:.*name'):
            Project.objects.create(name=test_name)
