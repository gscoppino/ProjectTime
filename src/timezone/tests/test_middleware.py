from django.test import SimpleTestCase
from django.test.client import RequestFactory
from django.utils import timezone
from ..middleware import TimezoneMiddleware


class TimezoneMiddlewareTestCase(SimpleTestCase):
    def test_activates_session_timezone(self):
        timezone_to_activate = 'America/New_York'
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.session = {'timezone': timezone_to_activate}

        def mock_get_response(request):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        self.assertNotEqual(timezone.get_current_timezone_name(),
                            timezone_to_activate)

        middleware.__call__(mock_request)
        self.assertEqual(timezone.get_current_timezone_name(),
                         timezone_to_activate)

    def test_does_nothing_if_no_session_timezone(self):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.session = {}

        def mock_get_response(request):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        expected_timezone = timezone.get_current_timezone()
        middleware.__call__(mock_request)
        self.assertEqual(timezone.get_current_timezone(),
                         expected_timezone)
