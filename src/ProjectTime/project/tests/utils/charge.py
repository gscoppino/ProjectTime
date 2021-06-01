from datetime import timedelta

from ProjectTime.project.models import Charge

from .general import get_start_of_today


class ChargeFactory:
    @classmethod
    def today(cls, project=None, charge_time=None):
        start_of_today = get_start_of_today()
        return Charge(project=project,
                      start_time=start_of_today,
                      end_time=start_of_today + charge_time)

    @classmethod
    def past_month(cls, project=None, charge_time=None):
        past_month = get_start_of_today() - timedelta(days=31)
        return Charge(project=project,
                      start_time=past_month,
                      end_time=past_month + charge_time)

    @classmethod
    def future_month(cls, project=None, charge_time=None):
        future_month = get_start_of_today() + timedelta(days=31)
        return Charge(project=project,
                      start_time=future_month,
                      end_time=future_month + charge_time)
