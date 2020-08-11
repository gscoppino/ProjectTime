from django.utils import timezone


def get_start_of_today():
    return timezone.now().replace(hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)
