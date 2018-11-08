import requests
import json

from app.storers.storer import Storer
from app.senders.team_in_match_sender import TeamInMatchSender
from app.models import TeamInMatch


class TeamInMatchStorer(Storer):
    def store(self, content):
        sender = TeamInMatchSender()
        json_response = requests.get('https://matchday-server.herokuapp.com/teams_in_matches/').content
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = sender.send(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_team_in_match_equal(self, api_player, player_to_store):
        return (api_player['match'] == player_to_store['match'] and
                api_player['team'] == player_to_store['team'] and
                api_player['is_host'] == player_to_store['is_host'])

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for team_in_match in endpoint_content:
            if self.__is_team_in_match_equal(team_in_match, content_to_store):
                is_inside_api = True
                content_to_store['internal_identifier'] = team_in_match['id']
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            TeamInMatch.objects.get(internal_identifier=content['internal_identifier'])
        except TeamInMatch.DoesNotExist:
            player_to_add = TeamInMatch(internal_identifier=content['internal_identifier'])
            player_to_add.save()
