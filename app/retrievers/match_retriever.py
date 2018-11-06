from app.retrievers import retriever
from app.models import Competition, Person
import json


class MatchesRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        match_list = json_content['matches']
        available_matches = list()
        for match in match_list:
            proper_match = self.__construct_proper_match(match)
            available_matches.append(proper_match)

        return available_matches
    
    def __construct_proper_match(self, match):
        competition_id = Competition.objects.get(external_identifier=match['competition']['id']).internal_identifier
        competition_uri = 'https://matchday-server.herokuapp.com/competitions/{}/'.format(competition_id)
        referee_id = Person.objects.get(external_identifier=match['referees'][0]['id']).internal_identifier
        referee_uri = 'https://matchday-server.herokuapp.com/people/{}/'.format(referee_id)
        home_team_goals = match['score']['']#
        away_team_goals = match['score']['']#
        proper_match = {
            'date': match['utcDate'],
            'referee': referee_uri,
            'competition': competition_uri,
            'external_identifier': match['id'],
            'duration': match['duration'].lower(),
            'stage': match['stage'].lower(),
            'matchday': match['matchday'],
            'home_team_external_id': match['homeTeam']['id'],
            'away_team_external_id': match['awayTeam']['id'],
            'home_team_goals': home_team_goals,
            'away_team_goals': away_team_goals,
            'status': match['status'].lower()
        }
        return proper_match