import logging

import click

from kiririn.rasa import train

logger = logging.getLogger(__name__)


@click.command('train',
               help='run trainer and generate models')
@click.pass_context
def cli(ctx):
    logger.info('Training data')
    rasa_section = ctx.obj['rasa']
    return train(rasa_section['data'], rasa_section['config'],
                 rasa_section['models'])
