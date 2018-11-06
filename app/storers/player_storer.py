import requests
import json

from app.storers.storer import Storer
from app.senders.player_sender import PlayerSender
from app.models import Player


class PlayerStorer(Storer):
    def store(self, content):
        sender = PlayerSender()
        json_response = requests.get('https://matchday-server.herokuapp.com/players/').content
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = sender.send(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_player_equal(self, api_player, player_to_store):
        return (api_player['position'] == player_to_store['position'] and
                api_player['shirt_number'] == player_to_store['shirt_number'] and
                api_player['team'] == player_to_store['team'] and
                api_player['person'] == player_to_store['person'])

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for player in endpoint_content:
            if self.__is_player_equal(player, content_to_store):
                is_inside_api = True
                content_to_store['internal_identifier'] = player['id']
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            Player.objects.get(internal_identifier=content['internal_identifier'])
        except Player.DoesNotExist:
            player_to_add = Player(internal_identifier=content['internal_identifier'],
                                   internal_person_identifier=content['internal_person_identifier'])
            player_to_add.save()
