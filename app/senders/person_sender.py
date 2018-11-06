from app.senders import sender


class PersonSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'people/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
