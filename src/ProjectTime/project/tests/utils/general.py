from django.utils import timezone


class ValidationMixin:
    def assertValidationMessagePresent(self, errors, field, error_code):
        self.assertEqual(len(errors.keys()), 1)
        self.assertEqual(len(errors[field]), 1)
        self.assertEqual(errors[field][0].code, error_code)


def get_model_field(model_class, field_name):
    return model_class._meta.get_field(field_name)


def get_start_of_today():
    return timezone.now().replace(hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)
