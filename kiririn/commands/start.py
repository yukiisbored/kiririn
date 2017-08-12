import click

from kiririn.bot import start_bot


@click.command('start',
               help='start the bot')
@click.pass_context
def cli(ctx):
    return start_bot(ctx.obj)
