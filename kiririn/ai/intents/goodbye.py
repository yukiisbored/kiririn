from kiririn.ai.intents import Intent


class Goodbye(Intent):
    def process(self, msg, result):
        self.sender.sendMessage('See you later!')
