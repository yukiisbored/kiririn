import logging
import time

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

from kiririn.rasa import get_model, train

from telepot import Bot
from telepot.loop import MessageLoop

logger = logging.getLogger(__name__)

bot = None
interpreter = None

def handle(msg):
    pass

def start_bot(config):
    rasa_section = config['rasa']
    telegram_section = config['telegram']

    logger.info('Loading model')

    model = get_model(rasa_section)
    metadata = Metadata.load(model)

    logger.info('Loading interpreter')

    config = rasa_section['config']

    global interpreter
    interpreter = Interpreter.load(metadata,
                                   RasaNLUConfig(config))

    logger.info('Preparing Bot')

    global bot
    bot = Bot(telegram_section['token'])

    MessageLoop(bot, handle).run_as_thread()

    logger.info('Listening')

    while 1:
        time.sleep(10)
