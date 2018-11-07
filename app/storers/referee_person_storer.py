import requests
import json

from app.storers.storer import Storer
from app.senders.person_sender import PersonSender
from app.models import Person


class RefereePersonStorer(Storer):
    def store(self, content):
        if content['role'] != 'referee':
            return
        sender = PersonSender()
        json_response = requests.get('https://matchday-server.herokuapp.com/referees/').content
        endpoint_content = json.loads(json_response)
        is_inside_api = self.__is_inside_api(endpoint_content, content)
        if not is_inside_api:
            response_content = sender.send(content)
            content['internal_identifier'] = json.loads(response_content)['id']
        self.__store_to_db(content)

    def __is_person_equal(self, api_person, person_to_store):
        return api_person['name'] == person_to_store['name'] and \
               api_person['birth_date'] == person_to_store['birth_date']

    def __is_inside_api(self, endpoint_content, content_to_store):
        is_inside_api = False
        for person in endpoint_content:
            if self.__is_person_equal(person, content_to_store):
                is_inside_api = True
                content_to_store['internal_identifier'] = person['id']
                break
        return is_inside_api

    def __store_to_db(self, content):
        try:
            Person.objects.get(name=content['name'],
                               external_identifier=content['external_identifier'])
        except Person.DoesNotExist:
            person_to_add = Person(external_identifier=content['external_identifier'],
                                   internal_identifier=content['internal_identifier'],
                                   name=content['name'],
                                   role=content['role'])
            person_to_add.save()
