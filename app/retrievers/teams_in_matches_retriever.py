from app.retrievers import retriever

from app.models import Team, Person


class TeamsInMatchesRetriever(retriever.Retriever):
    def retrieve(self, content):
        proper_teams_in_matches = list()
        for match in content:
            proper_home_team_in_match = self.__construct_proper_home_teams_in_match(match)
            proper_away_team_in_match = self.__construct_proper_away_teams_in_match(match)
            proper_teams_in_matches.append(proper_home_team_in_match)
            proper_teams_in_matches.append(proper_away_team_in_match)
        return proper_teams_in_matches

    def __get_match_uri(self, match):
        match_id = match.external_identifier
        match_uri = 'https://matchday-server.herokuapp.com/matches/{}/'.format(match_id)
        return match_uri

    def __get_team_uri(self, external_team_id):
        try:
            team_id = Team.objects.get(external_identifier=external_team_id).internal_identifier
        except Team.DoesNotExist:
            return None
        team_uri = 'https://matchday-server.herokuapp.com/teams/{}/'.format(team_id)
        return team_uri

    def __get_coach_uri(self, external_team_id):
        try:
            coach_id = Person.objects.get(external_team_identifier=external_team_id, role='coach').internal_identifier
        except Person.DoesNotExist:
            return None
        coach_uri = 'https://matchday-server.herokuapp.com/people/{}/'.format(coach_id)
        return coach_uri

    def __construct_proper_team_in_match(self, match, external_team_id, is_host):
        proper_teams_in_match = {
            'is_host': is_host,
            'team': self.__get_team_uri(external_team_id),
            'match': self.__get_match_uri(match),
            'coach': self.__get_coach_uri(external_team_id)
        }
        return proper_teams_in_match

    def __construct_proper_home_teams_in_match(self, match):
        external_team_id = match.home_team_external_id
        home_team_in_match = self.__construct_proper_team_in_match(match, external_team_id, True)
        if match.home_team_goals:
            home_team_in_match['goals'] = match.home_team_goals
        else:
            home_team_in_match['goals'] = 0
        return home_team_in_match

    def __construct_proper_away_teams_in_match(self, match):
        external_team_id = match.away_team_external_id
        away_team_in_match = self.__construct_proper_team_in_match(match, external_team_id, False)
        if match.away_team_goals:
            away_team_in_match['goals'] = match.away_team_goals
        else:
            away_team_in_match['goals'] = 0
        return away_team_in_match
