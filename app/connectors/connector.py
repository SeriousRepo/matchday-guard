import requests
from app.constants import FOOTBALL_DATA_KEY


def connect(uri):
    credentials = {'X-Auth-Token': FOOTBALL_DATA_KEY}
    response = requests.get(uri, headers=credentials)
    if response.status_code is 200:
        return response.content
    else:
        response.raise_for_status()
