from app.senders import sender


class TeamSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'teams/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
