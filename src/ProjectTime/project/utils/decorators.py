def with_attrs(**attrs):
    def set_attrs(function):
        for key, value in attrs.items():
            setattr(function, key, value)

        return function

    return set_attrs
