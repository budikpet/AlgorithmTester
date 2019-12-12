import click
import itertools
from typing import Dict, List, Tuple
from algorithm_tester.tester_dataclasses import DynamicClickOption
from algorithm_tester.plugins import plugins

def validate_algorithms(self, ctx, value: str) -> List[str]:
    try:
        values = [c.strip() for c in value.split(",")]
        for out_value in values:
            if out_value not in plugins.get_algorithm_names():
                raise click.BadParameter(value)

        return values
    except:
        raise click.BadParameter(value)

def validate_parser(self, ctx, value: str) -> str:
    try:
        if value not in plugins.get_parser_names():
            raise click.BadParameter(value)

        return value
    except:
        raise click.BadParameter(value)

def validate_extra_options(self, ctx, value: List[str]) -> Dict[str, object]:
    try:
        output: Dict[str, object] = dict()
        dynamic_options: List[DynamicClickOption] = plugins.get_dynamic_options()
        # option_names: List[str] = [option.short_opt for option in dynamic_options]
        # option_names.extend([option.long_opt for option in dynamic_options])

        it = iter(value)
        values: List[Tuple[str, str]] = [(name.strip("-"), data) for name, data in list(zip(it, it))]

        for pair in values:
            # Find a dynamic option that has the same short or long name
            predicate = lambda option: option.short_opt == pair[0] or option.long_opt == pair[0]
            found_option = list(itertools
                .takewhile(predicate, dynamic_options))
            
            if len(found_option) <= 0:
                # This option does not exist
                raise click.BadParameter()
            
            found_option: DynamicClickOption = found_option[0]
            
            # Try using an appropriate data type
            if issubclass(found_option.data_type, int):
                output[found_option.name] = int(pair[1])
            elif issubclass(found_option.data_type, float):
                output[found_option.name] = float(pair[1])
            else:
                output[found_option.name] = pair[1]


        return output
    except:
        raise click.BadParameter(value)