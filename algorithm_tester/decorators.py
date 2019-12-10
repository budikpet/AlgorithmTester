def docstring_parameters(*args, **kwargs):
    """ A decorator that enables parameterized docstring. """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return dec