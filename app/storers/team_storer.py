import json

from app.storers.storer import Storer
from app.connectors.matchday.connector import Connector
from app.models import Team


class TeamStorer(Storer):
    __url_sufix = 'teams/'

    def store(self, content):
        connector = Connector(self.__url_sufix)
        json_response = connector.send_get()
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = connector.send_post(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_team_equal(self, api_team, team_to_store):
        return api_team['name'] == team_to_store['name'] and \
               api_team['stadium'] == team_to_store['stadium']

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for team in endpoint_content:
            if self.__is_team_equal(team, content_to_store):
                is_inside_api = True
                content_to_store['internal_identifier'] = team['id']
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            Team.objects.get(name=content['name'], stadium=content['stadium'])
        except Team.DoesNotExist:
            team_to_add = Team(internal_identifier=content['internal_identifier'],
                               external_identifier=content['external_identifier'],
                               name=content['name'],
                               stadium=content['stadium'])
            team_to_add.save()
