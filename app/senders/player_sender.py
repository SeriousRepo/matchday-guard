from app.senders import sender


class PlayerSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'players/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
