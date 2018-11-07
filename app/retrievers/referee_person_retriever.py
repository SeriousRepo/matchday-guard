import json

from app.retrievers import retriever


class RefereePersonRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        list_content = json.loads(content)
        matches = list_content['matches']
        proper_people = list()
        for match in matches:
            referees = match['referees']
            if referees:
                proper_person = self.__construct_proper_person(referees[0])
                proper_people.append(proper_person)

        return proper_people

    def __construct_proper_person(self, person):
        proper_person = {
            'external_identifier': person['id'],
            'name': person['name'],
            'role': 'referee',
            'nationality': person['nationality'],
            'birth_date': None
        }
        return proper_person
