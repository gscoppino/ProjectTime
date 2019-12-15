from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.test import SimpleTestCase
from django.test.client import RequestFactory
from unittest.mock import MagicMock, patch
from ..middleware import ProjectTimeTimezoneWarningMiddleware


def mock_add_warning_message():
    return MagicMock(return_value=None)


class ProjectTimeTimezoneWarningMiddlewareTestCase(SimpleTestCase):
    @patch.object(messages, 'warning', new_callable=mock_add_warning_message)
    def test_warns_user_if_no_active_timezone(self, mock_add_warning_message):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.user = User()
        mock_request.session = {}

        def mock_get_response(request):
            pass

        middleware = ProjectTimeTimezoneWarningMiddleware(mock_get_response)
        self.assertFalse(mock_add_warning_message.called)

        middleware.__call__(mock_request)
        self.assertTrue(mock_add_warning_message.called)
        self.assertEqual(mock_add_warning_message.call_count, 1)

    @patch.object(messages, 'warning', new_callable=mock_add_warning_message)
    def test_does_not_warn_user_if_active_timezone(self, mock_method):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.user = User()
        mock_request.session = {'timezone': 'America/New_York'}

        def mock_get_response(request):
            pass

        middleware = ProjectTimeTimezoneWarningMiddleware(mock_get_response)
        self.assertFalse(mock_method.called)

        middleware.__call__(mock_request)
        self.assertFalse(mock_method.called)

    @patch.object(messages, 'warning', new_callable=mock_add_warning_message)
    def test_does_not_warn_user_when_request_in_warning_whitelist(self, mock_method):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.user = User()
        mock_request.session = {}

        def mock_get_response(request):
            pass

        middleware = ProjectTimeTimezoneWarningMiddleware(mock_get_response)
        middleware.message_whitelist = (
            '/foo/bar',
        )
        self.assertFalse(mock_method.called)

        middleware.__call__(mock_request)
        self.assertFalse(mock_method.called)

    @patch.object(messages, 'warning', new_callable=mock_add_warning_message)
    def test_does_not_warn_user_when_user_is_not_authenticated(self, mock_method):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.user = AnonymousUser()
        mock_request.session = {}

        def mock_get_response(request):
            pass

        middleware = ProjectTimeTimezoneWarningMiddleware(mock_get_response)
        self.assertFalse(mock_method.called)

        middleware.__call__(mock_request)
        self.assertFalse(mock_method.called)
