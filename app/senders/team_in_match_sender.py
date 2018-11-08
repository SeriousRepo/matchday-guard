from app.senders import sender


class TeamInMatchSender(sender.Sender):
    def __init__(self):
        self.url = self.base_url + 'teams_in_matches/'

    def send(self, content):
        return self._send_to_uri(content, self.url)
