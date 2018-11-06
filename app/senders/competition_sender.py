from app.senders import sender


class CompetitionSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'competitions/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
