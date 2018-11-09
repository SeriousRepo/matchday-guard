from app.models import *
from app.connectors.football_data.connector import Connector
from app.retrievers.competition_retriever import CompetitionRetriever
from app.retrievers.team_retriever import TeamRetriever
from app.retrievers.non_referee_person_retriever import NonRefereePersonRetriever
from app.retrievers.referee_person_retriever import RefereePersonRetriever
from app.retrievers.player_retriever import PlayerRetriever
from app.retrievers.match_retriever import MatchesRetriever
from app.retrievers.teams_in_matches_retriever import TeamsInMatchesRetriever
from app.storers.competition_storer import CompetitionStorer
from app.storers.referee_person_storer import RefereePersonStorer
from app.storers.team_storer import TeamStorer
from app.storers.non_referee_person_storer import NonRefereePersonStorer
from app.storers.player_storer import PlayerStorer
from app.storers.match_storer import MatchStorer
from app.storers.team_in_match_storer import TeamInMatchStorer


class Scheduler:
    def compose_competitions(self):
        connector = Connector()
        content = connector.send_get('competitions?plan=TIER_ONE')
        retriever = CompetitionRetriever()
        competitions = retriever.retrieve(content)
        storer = CompetitionStorer()
        for competition in competitions:
            storer.store(competition)

    def compose_teams(self):
        retriever = TeamRetriever()
        storer = TeamStorer()
        connector = Connector()
        for i in range(1, Competition.objects.all().count() + 1):
            content = connector.send_get('competitions/{}/teams'.format(Competition.objects.get(pk=i).external_identifier))
            teams = retriever.retrieve(content)
            for team in teams:
                storer.store(team)

    def compose_team_squads(self):
        retriever = NonRefereePersonRetriever()
        storer = NonRefereePersonStorer()
        connector = Connector()
        for i in range(1, Team.objects.all().count() + 1):
            content = connector.send_get('teams/{}'.format(Team.objects.get(pk=i).external_identifier))
            people = retriever.retrieve(content)
            for person in people:
                storer.store(person)

    def compose_players(self):
        content = Person.objects.all()
        retriever = PlayerRetriever()
        players = retriever.retrieve(content)
        storer = PlayerStorer()
        for player in players:
            storer.store(player)

    def compose_referees_and_matches(self):
        referee_retriever = RefereePersonRetriever()
        matches_retriever = MatchesRetriever()
        referee_storer = RefereePersonStorer()
        match_storer = MatchStorer()
        connector = Connector()
        for i in range(1, Competition.objects.all().count() + 1):
            content = connector.send_get('competitions/{}/matches/'.format(Competition.objects.get(pk=i).external_identifier))
            referees = referee_retriever.retrieve(content)
            for referee in referees:
                referee_storer.store(referee)
            matches = matches_retriever.retrieve(content)
            for match in matches:
                match_storer.store(match)

    def compose_teams_in_match(self):
        content = Match.objects.all()
        retriever = TeamsInMatchesRetriever()
        teams = retriever.retrieve(content)
        storer = TeamInMatchStorer()
        for team in teams:
            storer.store(team)
