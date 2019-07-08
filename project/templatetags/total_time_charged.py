from django.template import Library
from datetime import timedelta

register = Library()


def total_time_charged(cl):
    total_time = timedelta()

    for charge in cl.result_list:
        total_time += charge.time_charged

    return {'total': total_time}


total_time_charged = register.inclusion_tag(
    'total_time_charged.html')(total_time_charged)
