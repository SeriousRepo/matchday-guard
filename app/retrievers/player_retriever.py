from app.retrievers import retriever

from app.models import Team


class PlayerRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        proper_players = list()
        for player in content:
            if player.role != 'player':
                continue
            proper_player = self.__construct_proper_player(player)
            proper_players.append(proper_player)
        return proper_players

    def __construct_proper_player(self, player):
        person_uri = 'https://matchday-server.herokuapp.com/people/{}/'.format(player.internal_identifier)
        team_id = Team.objects.get(external_identifier=player.external_team_identifier).internal_identifier
        team_uri = 'https://matchday-server.herokuapp.com/teams/{}/'.format(team_id)
        proper_player = {
            'internal_person_identifier': player.internal_identifier,
            'role': player.role,
            'position': player.position,
            'shirt_number': player.shirt_number,
            'person': person_uri,
            'team': team_uri
        }
        return proper_player
