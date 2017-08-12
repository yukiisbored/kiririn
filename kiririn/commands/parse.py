import logging
import os

import click
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

logger = logging.getLogger(__name__)


def get_newest_model(model_dir):
    models = os.listdir(model_dir)
    models.sort(reverse=True)

    model = models[0]

    if not model.startswith('model_'):
        raise 'No models found, Please train first to generate models'

    return os.path.join(model_dir, models[0])


@click.command('parse',
               help='parse text to structured data')
@click.argument('text', type=str)
@click.pass_context
def cli(ctx, text):
    rasa_section = ctx.obj['rasa']

    model = get_newest_model(rasa_section['models'])

    if 'model' in rasa_section:
        model = rasa_section['model']

    metadata = Metadata.load(model)
    interpreter = Interpreter.load(metadata,
                                   RasaNLUConfig(rasa_section['config']))

    logger.info(interpreter.parse(text))
