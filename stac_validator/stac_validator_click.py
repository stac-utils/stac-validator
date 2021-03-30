import click


class StacValidate:
    def __init__(
        self,
        stac_file: str,
    ):
        pass

    @click.group()
    def cli():
        pass

    @click.command()
    @click.argument("stac_file", type=click.Path(exists=True))
    def validate(stac_file):
        """Print FILENAME if the file exists."""
        click.echo(click.format_filename(stac_file))

    # @click.command()
    # @click.option('--verbose', is_flag=True, help="Will print verbose messages.")
    # @click.option('--name', '-n', multiple=True, default='', prompt='Your name', help="Who are you?")
    # @click.argument('country')
    # def hello(verbose, name, country):
    #     """This is an example script to learn Click."""
    #     if verbose:
    #         click.echo("We are in the verbose mode.")
    #     click.echo('Hello {0}'.format(country))
    #     for n in name:
    #         click.echo('Bye {0}'.format(n))


if __name__ == "__main__":
    # cli.add_command(hello)
    stac_val = StacValidate("")
    stac_val.cli.add_command(stac_val.validate)
    stac_val.cli()
