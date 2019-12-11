import click
from typing import Dict, List
from algorithm_tester.tester_dataclasses import DynamicClickOption

def docstring_parameters(*args, **kwargs):
    """ A decorator that enables parameterized docstring. """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return dec

def use_dynamic_options(options: List[DynamicClickOption]):
    def decorator(f):
        for dynamic_option in reversed(options):
            dynamic_option: DynamicClickOption = dynamic_option
            param_decls = (
                '-' + dynamic_option.short_opt,
                '--' + dynamic_option.long_opt,
                dynamic_option.name)
            attrs = dict(
                required=dynamic_option.required,
                type=dynamic_option.data_type,
                help=dynamic_option.doc_help
            )

            click.option(*param_decls, **attrs)(f)
        return f

    return decorator