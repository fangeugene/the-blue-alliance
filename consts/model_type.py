from models.award import Award
from models.event import Event
from models.event_team import EventTeam
from models.match import Match
from models.media import Media
from models.team import Team


class ModelType(object):
    """
    Enums for the different model types
    Note that only certain models are actually instantiated in the DB
    DO NOT CHANGE EXISTING ONES
    """

    EVENT = 0
    TEAM = 1
    MATCH = 2
    EVENT_TEAM = 3
    DISTRICT = 4
    DISTRICT_TEAM = 5
    AWARD = 6
    MEDIA = 7

    to_type = {
        Event: EVENT,
        Team: TEAM,
        Match: MATCH,
        EventTeam: EVENT_TEAM,
        Award: AWARD,
        Media: MEDIA,

    }

    to_type_from_kind = {
        'Event': EVENT,
        'Team': TEAM,
        'Match': MATCH,
        'EventTeam': EVENT_TEAM,
        'Award': AWARD,
        'Media': MEDIA,
    }

    from_type = {
        EVENT: Event,
        TEAM: Team,
        MATCH: Match,
        EVENT_TEAM: EventTeam,
        AWARD: Award,
        MEDIA: Media,
    }
