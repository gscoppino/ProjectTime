""" Django middlewares for timezone Django app.
"""

from django.utils import timezone as django_timezone
from pytz import timezone


class TimezoneMiddleware:  # pylint: disable=too-few-public-methods
    """ Middleware that activates the selected timezone for a user session on
        every request.
    """

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'timezone' in request.session:
            django_timezone.activate(timezone(request.session['timezone']))

        # Call the next middleware (or the view, if this is the last middleware)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
