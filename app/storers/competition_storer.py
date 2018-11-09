import json

from app.storers.storer import Storer
from app.connectors.matchday.connector import Connector
from app.models import Competition


class CompetitionStorer(Storer):
    __url_sufix = 'competitions/'

    def store(self, content):
        connector = Connector(self.__url_sufix)
        json_response = connector.send_get()
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = connector.send_post(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_competition_equal(self, api_competition, competition_to_store):
        return api_competition['name'] == competition_to_store['name'] and \
               api_competition['year'] == competition_to_store['year']

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for competition in endpoint_content:
            if self.__is_competition_equal(competition, content_to_store):
                is_inside_api = True
                content_to_store['internal_identifier'] = competition['id']
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            Competition.objects.get(name=content['name'], year=content['year'])
        except Competition.DoesNotExist:
            competition_to_add = Competition(internal_identifier=content['internal_identifier'],
                                             external_identifier=content['external_identifier'],
                                             name=content['name'],
                                             area_id=content['area_id'],
                                             year=content['year'])
            competition_to_add.save()
