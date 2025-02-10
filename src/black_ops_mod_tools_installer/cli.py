import click


@click.group()
def cli():
    pass


@click.command(name='cli')
def cli():
    click.echo("Launching cli...")


@click.option(
    '--content_pack_tomls',
    default=[],
    help='A list of content pack toml names/paths.',
    multiple=True
)    


@click.command(name='tui')
def tui_default():
    click.echo("Launching tui...")
