import requests
from app.constants import FOOTBALL_DATA_KEY, FOOTBALL_DATA_URL


class Connector:
    __headers = {'X-Auth-Token': FOOTBALL_DATA_KEY}
    __base_url = FOOTBALL_DATA_URL

    def send_get(self, url):
        response = requests.get(self.__base_url + url, headers=self.__headers)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.content
