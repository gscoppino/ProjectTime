def validate_and_save(model_instance, clean_kwargs={}, save_kwargs={}):
    # NOTE: This method is generic and useful enough that it could moved out into an application utility library.
    model_instance.full_clean(**clean_kwargs)
    model_instance.save(**save_kwargs)

    return model_instance
