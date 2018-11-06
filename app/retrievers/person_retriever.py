import json

from app.retrievers import retriever


class PersonRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        dict_content = json.loads(content)
        team_id = dict_content['id']
        squad = dict_content['squad']
        proper_people = list()
        for person in squad:
            proper_person = self.__construct_proper_person(person)
            proper_person['external_team_identifier'] = team_id
            proper_people.append(proper_person)
        return proper_people

    def __construct_proper_person(self, person):
        birth_date = None
        if person['dateOfBirth']:
            birth_date = person['dateOfBirth'][0:10]
        proper_person = {
            'external_identifier': person['id'],
            'name': person['name'],
            'role': person['role'].lower(),
            'position': person['position'],
            'birth_date': birth_date,
            'nationality': person['nationality'],
            'shirt_number': person['shirtNumber']
        }
        return proper_person
