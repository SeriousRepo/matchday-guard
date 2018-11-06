from app.retrievers import retriever
import json


class TeamRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        teams = json_content['teams']
        available_teams = list()
        for team in teams:
            proper_team = self.__construct_proper_team(team)
            available_teams.append(proper_team)
        return available_teams

    def __construct_proper_team(self, team):
        crest_uri = None
        if team['crestUrl'] != '':
            crest_uri = team['crestUrl']
        proper_team = {
            'name': team['name'],
            'stadium': team['venue'],
            'crest_url': crest_uri,
            'external_identifier': team['id']
        }
        return proper_team
