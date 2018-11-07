from django.http import HttpResponse

from app.schedulers.scheduler import Scheduler


def index(request):
    scheduler = Scheduler()
    #scheduler.compose_competitions()
    #scheduler.compose_teams()
    #scheduler.compose_team_squads()
    #scheduler.compose_players()
    scheduler.compose_referees_and_matches()
    return HttpResponse("Hello, world. You're at the polls index.")
