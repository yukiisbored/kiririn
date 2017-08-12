import logging
import os

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
import rasa_nlu.model as rm

logger = logging.getLogger(__name__)


def train(data, config, models, training_data=None, trainer=None):
    rm.logger = logger
    if training_data is None:
        training_data = load_data(data)

    if trainer is None:
        trainer = rm.Trainer(RasaNLUConfig(config))

    trainer.train(training_data)
    model_directory = trainer.persist(models)


def get_newest_model(model_dir):
    models = os.listdir(model_dir)
    models.sort(reverse=True)

    model = models[0]

    if not model.startswith('model_'):
        raise 'No models found, Please train first to generate models'

    return os.path.join(model_dir, models[0])


def parse(text, model, config, metadata=None, interpreter=None):
    if metadata is None:
        metadata = rm.Metadata.load(model)

    if interpreter is None:
        interpreter = rm.Interpreter.load(metadata,
                                          RasaNLUConfig(config))

    return interpreter.parse(text)
