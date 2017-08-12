import logging

import click

from kiririn.rasa import get_newest_model, parse

logger = logging.getLogger(__name__)


@click.command('parse',
               help='parse text to structured data')
@click.argument('text', type=str)
@click.pass_context
def cli(ctx, text):
    rasa_section = ctx.obj['rasa']

    config = rasa_section['config']
    model = get_newest_model(rasa_section['models'])

    if 'model' in rasa_section:
        model = rasa_section['model']

    logger.info(parse(text, model, config))
