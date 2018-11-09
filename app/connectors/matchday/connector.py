from app.constants import MATCHDAY_SERVER_KEY, MATCHDAY_BASE_URL
import json
import requests


class Connector:
    __base_url = MATCHDAY_BASE_URL
    __headers = {'content-type': 'application/json',
                 'authorization': 'Token {}'.format(MATCHDAY_SERVER_KEY)}

    def __init__(self, url_sufix):
        self.url = self.__base_url + url_sufix
    
    def send_post(self, content):
        json_content = json.dumps(content)
        response = requests.request("POST", self.url, data=json_content, headers=self.__headers)

        if response.status_code != 201:
            print(response.text)
            response.raise_for_status()

        return response.content
    
    def send_put(self, content):
        json_content = json.dumps(content)
        response = requests.request('PUT', self.url, data=json_content, headers=self.__headers)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.content
    
    def send_get(self):
        response = requests.request('GET', self.url, headers=self.__headers)

        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()

        return response.content
    
    def send_delete(self):
        response = requests.request('DELETE', self.url, headers=self.__headers)

        if response.status_code != 204:
            print(response.text)
            response.raise_for_status()

        return response.content
