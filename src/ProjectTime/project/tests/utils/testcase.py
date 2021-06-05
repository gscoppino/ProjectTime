from django.contrib.auth.models import User
from django.test import TestCase


class AdminUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('test', '', 'test')

    # Helper methods
    def performLogin(self):
        logged_in = self.client.login(username='test', password='test')
        if not logged_in:
            self.fail('Unable to login.')
