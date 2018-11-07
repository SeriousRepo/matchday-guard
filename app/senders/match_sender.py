from app.senders import sender


class MatchSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'matches/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
