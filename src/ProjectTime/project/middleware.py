""" Django middlewares for the project Django app
"""

from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe


class ProjectTimeTimezoneWarningMiddleware:  # pylint: disable=too-few-public-methods
    """ Middleware that uses the Django messages framework to display a warning
        when a user is logged in without having set a timezone for their
        user session.
    """
    message_tag = 'no_timezone_msg'
    message_whitelist = (
        reverse_lazy('admin:select-timezone'),
        reverse_lazy('admin:logout')
    )

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if 'text/html' not in request.headers.get('Accept', ''):
            return self.get_response(request)

        if 'timezone' in request.session:
            return self.get_response(request)

        if request.path_info in self.message_whitelist:
            return self.get_response(request)

        has_message = any(message for message in messages.get_messages(request)
                          if message.extra_tags == self.message_tag)

        if has_message:
            return self.get_response(request)

        # Warn the user that they have not specified a timezone
        # and prompt them to do so.
        url = reverse('admin:select-timezone')
        messages.warning(
            request,
            mark_safe(
                'Timezone has not been specified. '
                f'<a href="{url}">Change Timezone</a> '
                'to the desired timezone.'
            ),
            extra_tags=self.message_tag
        )

        return self.get_response(request)
