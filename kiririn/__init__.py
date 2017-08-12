import configparser
import os
import logging

import click
import click_log


logger = logging.getLogger(__name__)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class KiririnCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__('kiririn.commands.' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=KiririnCLI)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.option('--config', '-c', envvar='KIRIRIN_CONFIG',
              type=click.Path(dir_okay=False),
              default='config.ini',
              help='configuration file to be used, defaults to config.ini')
@click.pass_context
def cli(ctx, config):
    ctx.obj = configparser.ConfigParser()
    ctx.obj.read(config)
