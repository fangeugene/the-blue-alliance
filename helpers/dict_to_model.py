from models.event import Event
from models.team import Team


class DictToModel(object):
    @classmethod
    def teamConverter(cls, team_dict):
        return Team(
            id=team_dict['key'],
            team_number=team_dict['team_number'],
            name=team_dict['name'],
            nickname=team_dict['nickname'],
            website=team_dict['website'],
            rookie_year=team_dict['rookie_year'],
        )

    @classmethod
    def eventConverter(cls, event_dict):
        pass
