from app.models import *
from app.connectors.connector import connect
from app.retrievers.competition_retriever import CompetitionRetriever
from app.retrievers.team_retriever import TeamRetriever
from app.retrievers.person_retriever import PersonRetriever
from app.retrievers.player_retriever import PlayerRetriever
from app.storers.competition_storer import CompetitionStorer
from app.storers.team_storer import TeamStorer
from app.storers.person_storer import PersonStorer
from app.storers.player_storer import PlayerStorer


class Scheduler:
    def compose_competitions(self):
        content = connect('http://api.football-data.org/v2/competitions?plan=TIER_ONE')
        retriever = CompetitionRetriever()
        competitions = retriever.retrieve(content)
        storer = CompetitionStorer()
        for competition in competitions:
            storer.store(competition)

    def compose_teams(self):
        for i in range(1, Competition.objects.all().count() + 1):
            content = connect('http://api.football-data.org/v2/competitions/{}/teams'.format(Competition.objects.get(pk=i).external_identifier))
            retriever = TeamRetriever()
            teams = retriever.retrieve(content)
            storer = TeamStorer()
            for team in teams:
                storer.store(team)

    def compose_team_squads(self):
        for i in range(1, Team.objects.all().count() + 1):
            content = connect('http://api.football-data.org/v2/teams/{}'.format(Team.objects.get(pk=i).external_identifier))
            retriever = PersonRetriever()
            people = retriever.retrieve(content)
            storer = PersonStorer()
            for person in people:
                storer.store(person)

    def compose_players(self):
        content = Person.objects.all()
        retriever = PlayerRetriever()
        players = retriever.retrieve(content)
        storer = PlayerStorer()
        for player in players:
            storer.store(player)
