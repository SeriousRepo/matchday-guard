from app.constants import MATCHDAY_SERVER_KEY
import json
import requests


class Sender:
    base_url = 'https://matchday-server.herokuapp.com/'
    headers = {'content-type': 'application/json',
               'authorization': 'Token {}'.format(MATCHDAY_SERVER_KEY)}
    
    def _send_to_uri(self, content, url):
        json_content = json.dumps(content)
        response = requests.request("POST", url, data=json_content, headers=self.headers)

        if response.status_code != 201:
            print(response.text)
            response.raise_for_status()

        return response.content
