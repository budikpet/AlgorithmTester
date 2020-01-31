import click
from typing import Dict, List
from algorithm_tester_common.tester_dataclasses import DynamicClickOption, Algorithm, Parser, Communicator
from algorithm_tester.concurrency_runners import Runner, Runners

"""
Contains all helper decorators.
"""

__help_full_info: str = "\b\n{name}:\n    {doc}"
__help_short_info: str = "\b\nAvailable {title}:    [{names}]"

def __get_full_info_strings(title: str, objects_list: List[object]):
    full_infos: List[str] = [f'{title.upper()}:']

    for alg in objects_list:
        full_infos.append(__help_full_info.format(name=alg.get_name(), doc=alg.__doc__.strip()))

    return full_infos

def dynamic_help(algorithms: List[Algorithm], parsers: List[Parser], communicators: List[Communicator]):
    """
    A decorator for Click interface. Creates more detailed help string.
    
    Arguments:
        algorithms {List[Algorithm]} -- All available algorithms.
        parsers {List[Parser]} -- All available parsers.
        communicators {List[Communicator]} -- All available communicators.
    
    """
    def dec(obj):
        runners = [(r.name, r.value) for r in Runners]
        runners_full_infos: List[str] = ["RUNNERS:"]
        runners_short_infos: str = __help_short_info.format(title="runners", names=", ".join([r[0].lower() for r in runners]))
        for (name, runner) in runners:
            runners_full_infos.append(__help_full_info.format(name=name.lower(), doc=runner.__doc__.strip()))

        algorithm_full_infos: List[str] = __get_full_info_strings("ALGORITHMS", algorithms)
        algorithm_short_infos: str = __help_short_info.format(title="algorithms", names=", ".join([alg.get_name() for alg in algorithms]))
        parsers_full_infos: List[str] = __get_full_info_strings("PARSERS", parsers)
        parsers_short_infos: str = __help_short_info.format(title="parsers", names=", ".join([p.get_name() for p in parsers]))
        communicators_full_infos: List[str] = __get_full_info_strings("COMMUNICATORS", communicators)
        communicators_short_infos: str = __help_short_info.format(title="communicators", names=", ".join([c.get_name() for c in communicators]))
        joined_full_infos: List[str] = algorithm_full_infos + parsers_full_infos + communicators_full_infos + runners_full_infos
        joined_short_infos: List[str] = [algorithm_short_infos, parsers_short_infos, communicators_short_infos, runners_short_infos]

        help_string: str = '{full_info}\b\n\n\nSHORT_INFO:\n\n{short_info}'.format(full_info="\n\n".join(joined_full_infos), short_info="\n\n".join(joined_short_infos))

        obj.__doc__ = help_string
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