import logging

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from kiririn.rasa import get_model, train

logger = logging.getLogger(__name__)

metadata = None
interpreter = None


def start(bot, update):
    pass


def do(bot, update):
    pass


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"'.format(update, error))


def start_bot(config):
    rasa_section = config['rasa']
    telegram_section = config['telegram']

    logger.info('Loading model')

    model = get_model(rasa_section)
    metadata = Metadata.load(model)

    logger.info('Loading interpreter')

    config = rasa_section['config']
    interpreter = Interpreter.load(metadata,
                                   RasaNLUConfig(config))

    logger.info('Preparing Bot')

    updater = Updater(telegram_section['token'])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, do))

    dp.add_error_handler(error)

    logger.info('Starting Bot')

    updater.start_polling()

    logger.info('Bot started, Gonna idle')

    updater.idle()
