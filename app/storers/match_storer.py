import requests
import json

from app.storers.storer import Storer
from app.senders.match_sender import MatchSender
from app.models import Match


class MatchStorer(Storer):
    def store(self, content):
        sender = MatchSender()
        json_response = requests.get('https://matchday-server.herokuapp.com/matches/').content
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = sender.send(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_match_equal(self, api_match, match_to_store):
        return api_match['id'] == match_to_store['external_identifier']

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for match in endpoint_content:
            if self.__is_match_equal(match, content_to_store):
                is_inside_api = True
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            Match.objects.get(external_identifier=content['external_identifier'])
        except Match.DoesNotExist:
            match_to_add = Match(external_identifier=content['external_identifier'],
                                 home_team_external_id=content['home_team_external_id'],
                                 away_team_external_id=content['away_team_external_id'],
                                 home_team_goals=content['home_team_goals'],
                                 away_team_goals=content['away_team_goals'])

            match_to_add.save()
