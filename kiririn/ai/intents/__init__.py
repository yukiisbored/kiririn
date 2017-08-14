class Intent:
    def __init__(self, sender, config):
        self.sender = sender
        self.config = config

    def process(self, msg, result):
        raise NotImplementedError
