import os
from django.utils import timezone

def activate_timezone_for_cli():
    tz = os.environ.get("PROJECT_TIME_CLI_TIMEZONE")
    if not tz:
        tz = input("Enter a timezone: ")

    timezone.activate(tz)