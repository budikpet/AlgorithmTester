import click

@click.command()
@click.argument('source', nargs=-1, required=True)
@click.argument('target', required=True)
def cp(source, target):
	for s in source:
		click.echo(f'Copying {s} to {target}')


@click.command()
@click.option('--count', required=True, type=int, help='Number of greetings.')
@click.option('--name', '-n', prompt='Enter name: ', help='Name to greet', metavar='NAME')
@click.option('-c/-C', '--color/--no-color')
@click.option('-v', '--verbose', is_flag=True)
def hello(count, name, color, verbose):
	greeting = (f'Hello, {name}')
	if color:
		greeting = click.style(greeting, fg='green', bg='black')
	for x in range(count):
		click.echo(greeting)

# Toto bude použito při zavolání z CLI
if __name__ == '__main__':
	#hello()
	cp()
