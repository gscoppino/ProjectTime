from django.test import SimpleTestCase
from django.test.client import RequestFactory
from django.utils import timezone

from ProjectTime.timezone.middleware import TimezoneMiddleware


class TimezoneMiddlewareTestCase(SimpleTestCase):
    def test_activates_session_timezone(self):
        timezone_to_activate = 'America/New_York'
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.headers = {}
        mock_request.session = {'timezone': timezone_to_activate}

        def mock_get_response(*args):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        self.assertNotEqual(timezone.get_current_timezone_name(),
                            timezone_to_activate)

        middleware.__call__(mock_request)
        self.assertEqual(timezone.get_current_timezone_name(),
                         timezone_to_activate)
        
        timezone.deactivate()

    def test_activates_header_timezone(self):
        timezone_to_activate = 'America/New_York'
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.headers = {'tz': timezone_to_activate}
        mock_request.session = {}

        def mock_get_response(*args):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        self.assertNotEqual(timezone.get_current_timezone_name(),
                            timezone_to_activate)

        middleware.__call__(mock_request)
        self.assertEqual(timezone.get_current_timezone_name(),
                         timezone_to_activate)

        timezone.deactivate()

    def test_does_not_activate_invalid_header_timezone(self):
        timezone_to_activate = 'not_a_real_timezone'
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.headers = {'tz': timezone_to_activate}
        mock_request.session = {}

        def mock_get_response(*args):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        self.assertNotEqual(timezone.get_current_timezone_name(),
                            timezone_to_activate)

        middleware.__call__(mock_request)
        self.assertNotEqual(timezone.get_current_timezone_name(),
                         timezone_to_activate)

    def test_does_nothing_if_no_session_or_header_timezone(self):
        mock_request = RequestFactory().get('/foo/bar')
        mock_request.headers = {}
        mock_request.session = {}

        def mock_get_response(*args):
            pass

        middleware = TimezoneMiddleware(mock_get_response)
        expected_timezone = timezone.get_current_timezone()
        middleware.__call__(mock_request)
        self.assertEqual(timezone.get_current_timezone(),
                         expected_timezone)
