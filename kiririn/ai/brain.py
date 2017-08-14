import os
import logging

INTENTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              'intents'))

logger = logging.getLogger(__name__)


class Brain:
    def __init__(self, sender, interpreter, config):
        self.sender = sender
        self.interpreter = interpreter
        self.config = config

        logger.debug('B New Brain!')

        ints = dict()

        for name in self.list_intents():
            int = self.get_intent_class(name)
            ints[name] = int(sender, config)

        self.intents = ints

        logger.debug('B Loaded {} intents!'.format(len(ints)))

    def list_intents(self):
        ints = []
        for filename in os.listdir(INTENTS_FOLDER):
            if (filename.endswith('.py') and
                not (filename.startswith('__') or
                     filename.startswith('.'))):
                ints.append(filename[:-3])
        ints.sort()
        return ints

    def get_intent_class(self, name):
        class_name = name.title()
        try:
            mod = __import__('kiririn.ai.intents.' + name,
                             None, None, [class_name])
        except ImportError:
            return
        return getattr(mod, class_name)

    def get_intent(self, name):
        return self.intents[name]

    def confused(self, msg):
        self.sender.sendMessage(
            "I'm sorry, I don't know what you're trying to do.")

    def empty(self, msg):
        self.sender.sendMessage('Hi there, Do you need anything?')

    def process(self, msg):
        text = msg['text']
        result = self.interpreter.parse(text)

        intent_name = result['intent']['name']
        confidence = result['intent']['confidence']

        logger.debug('< {}'.format(text))
        logger.debug('? {} : {}%'.format(intent_name,
                                         confidence * 100))

        if confidence > 0.5:
            intent = self.get_intent(intent_name)
            return intent.process(msg, result)
        elif text:
            self.confused(msg)
        else:
            self.empty(msg)
