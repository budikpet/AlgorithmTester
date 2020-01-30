import click
from typing import Dict, List
from algorithm_tester_common.tester_dataclasses import DynamicClickOption, Algorithm, Parser, Communicator
from algorithm_tester.concurrency_runners import Runner

"""
Contains all helper decorators.
"""

def dynamic_help(algorithms: List[Algorithm], parsers: List[Parser], communicators: List[Communicator], runners: List[Runner]):
    def dec(obj):
        obj.__doc__ = "Help me"
        return obj
    return dec

def docstring_parameters(*args, **kwargs):
    """ A decorator that enables parameterized docstring. """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return dec

def use_dynamic_options(options: List[DynamicClickOption]):
    """
    Makes it possible to add dynamic options as valid Click CLI options.

    These options are shown and used as thought they were created by @click.option directly.
    
    Args:
        options (List[DynamicClickOption]): A list of dynamic options.
    
    Returns:
        func: A function that adds dynamic options through @click.option.
    """
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