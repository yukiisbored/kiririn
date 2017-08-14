import logging
import re
import time

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open

from kiririn.ai.brain import Brain
from kiririn.rasa import get_model

logger = logging.getLogger(__name__)


class KiririnHandler(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, interpreter, config, **kwargs):
        super(KiririnHandler, self).__init__(seed_tuple, **kwargs)

        logger.debug('! New Handler')

        self.interpreter = interpreter

        logger.debug('! Starting a new brain')

        self.brain = Brain(self.sender, interpreter, config)

        self._username = config['telegram']['username']

    def _get_mention_text(self):
        return '@' + self._username

    def _should_do_it(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text' or chat_type == 'channel':
            return False

        if chat_type == 'private':
            return True

        text = msg['text']

        return (text.startswith(self._get_mention_text()) or
                text.endswith(self._get_mention_text()))

    def _filter_text(self, text):
        text = re.sub('^{}\s*,?\s*'.format(self._get_mention_text()), '', text)
        text = re.sub('\s*,?\s*{}$'.format(self._get_mention_text()), '', text)
        return text

    def on_chat_message(self, msg):
        if not self._should_do_it(msg):
            return

        msg['text'] = self._filter_text(msg['text'])

        return self.brain.process(msg)


def start_bot(config):
    rasa_section = config['rasa']
    telegram_section = config['telegram']

    logger.info('Loading model')

    model = get_model(rasa_section)
    metadata = Metadata.load(model)

    logger.info('Loading interpreter')

    rasa_config = rasa_section['config']

    interpreter = Interpreter.load(metadata,
                                   RasaNLUConfig(rasa_config))

    logger.info('Preparing Bot')

    token = telegram_section['token']

    bot = telepot.DelegatorBot(token, [
        pave_event_space()(
            per_chat_id(), create_open,
            KiririnHandler, interpreter, config, timeout=20)
    ])

    MessageLoop(bot).run_as_thread()

    logger.info('Listening')

    while 1:
        time.sleep(10)
