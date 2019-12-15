from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe


class ProjectTimeTimezoneWarningMiddleware:
    message_whitelist = (
        reverse_lazy('admin:select-timezone'),
        reverse_lazy('admin:logout'),
        reverse_lazy('admin:jsi18n'),
    )

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if 'timezone' in request.session:
            return self.get_response(request)

        if request.path_info in self.message_whitelist:
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
            )
        )

        return self.get_response(request)
