from app.retrievers import retriever
import json


class CompetitionRetriever(retriever.Retriever):
    def __init__(self):
        pass

    def retrieve(self, content):
        json_content = json.loads(content)
        competitions = json_content['competitions']
        available_competitions = list()
        for competition in competitions:
            if competition['name'] not in ['Premier League', 'Primera Division']:  #
                continue                                                           # Todo Remove after adding more competitions
            proper_competition = self.__construct_proper_competition(competition)
            available_competitions.append(proper_competition)

        return available_competitions

    __competition_types = {
        'Série A': 'league',
        'Championship': 'league',
        'Premier League': 'league',
        'European Championship': 'tournament',
        'UEFA Champions League': 'tournament',
        'Ligue 1': 'league',
        'Bundesliga': 'league',
        'Serie A': 'league',
        'Eredivisie': 'league',
        'Primeira Liga': 'league',
        'Primera Division': 'league',
        'FIFA World Cup': 'tournament'
    }

    def __construct_proper_competition(self, competition):
        proper_competition = {
            'name': competition['name'],
            'type': self.__competition_types[competition['name']],
            'area': competition['area']['name'],
            'year': int(competition['currentSeason']['startDate'][0:4]),
            'external_identifier': competition['id'],
            'area_id': competition['area']['id']
        }
        return proper_competition
