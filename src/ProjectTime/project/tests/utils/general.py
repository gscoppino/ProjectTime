from django.utils import timezone

def get_start_of_today():
    return timezone.now().replace(hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)

def validate_and_save(model_instance, clean_kwargs=None, save_kwargs=None):
    # NOTE: This method is generic and useful enough that it could moved out into an application
    # utility library.

    if not clean_kwargs:
        clean_kwargs = {}

    if not save_kwargs:
        save_kwargs = {}

    model_instance.full_clean(**clean_kwargs)
    model_instance.save(**save_kwargs)

    return model_instance
