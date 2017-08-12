import logging

import click
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
import rasa_nlu.model

logger = logging.getLogger(__name__)


def train(data, config, models):
    training_data = load_data(data)
    trainer = rasa_nlu.model.Trainer(RasaNLUConfig(config))
    trainer.train(training_data)
    model_directory = trainer.persist(models)


@click.command('train',
               help='run trainer and generate models')
@click.pass_context
def cli(ctx):
    logger.info('Training data')
    rasa_nlu.model.logger = logger
    rasa_section = ctx.obj['rasa']
    return train(rasa_section['data'], rasa_section['config'],
                 rasa_section['models'])
