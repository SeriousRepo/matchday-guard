from app.retrievers import retriever
from app.models import Competition, Person
import json


class MatchesRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        external_competition_id = json_content['competition']['id']
        competition_uri = self.__get_competition_uri(external_competition_id)
        match_list = json_content['matches']
        available_matches = list()
        for match in match_list:
            proper_match = self.__construct_proper_match(match)
            proper_match['competition'] = competition_uri
            available_matches.append(proper_match)

        return available_matches

    def __get_competition_uri(self, external_competition_id):
        competition = Competition.objects.get(external_identifier=external_competition_id)
        competition_id = competition.internal_identifier
        competition_uri = 'https://matchday-server.herokuapp.com/competitions/{}/'.format(competition_id)
        return competition_uri

    def __get_result_key(self, duration):
        return {
            'regular': 'fullTime',
            'penalty_shootout': 'penalties',
            'extra_time': 'extraTime'
        }[duration]

    def __construct_proper_match(self, match):
        referee_uri = None
        if match['referees']:
            referee_id = Person.objects.get(external_identifier=match['referees'][0]['id']).internal_identifier
            referee_uri = 'https://matchday-server.herokuapp.com/people/{}/'.format(referee_id)
        result_key = self.__get_result_key(match['score']['duration'].lower())
        home_team_goals = match['score'][result_key]['homeTeam']
        away_team_goals = match['score'][result_key]['awayTeam']
        proper_match = {
            'id': match['id'],
            'date': match['utcDate'],
            'main_referee': referee_uri,
            'external_identifier': match['id'],
            'duration': match['score']['duration'].lower(),
            'stage': match['stage'].lower(),
            'group': match['group'].lower(),
            'matchday': match['matchday'],
            'home_team_external_id': match['homeTeam']['id'],
            'away_team_external_id': match['awayTeam']['id'],
            'home_team_goals': home_team_goals,
            'away_team_goals': away_team_goals,
            'status': match['status'].lower()
        }

        return proper_match
