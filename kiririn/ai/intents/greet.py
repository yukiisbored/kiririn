from kiririn.ai.intents import Intent


class Greet(Intent):
    def process(self, msg, result):
        self.sender.sendMessage('Hello!')
