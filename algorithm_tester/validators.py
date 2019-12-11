import click
from algorithm_tester.plugins import plugins

def validate_algorithms(self, ctx, value: str):
    try:
        values = [c.strip() for c in value.split(",")]
        for out_value in values:
            if out_value not in plugins.get_algorithm_names():
                raise click.BadParameter(value)

        return values
    except:
        raise click.BadParameter(value)