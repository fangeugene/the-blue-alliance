import json

from datetime import datetime
from google.appengine.ext import ndb

from api.v2.apibase import APIv2
from helpers.award_helper import AwardHelper
from helpers.district_helper import DistrictHelper
from helpers.model_to_dict import ModelToDict
from models.event import Event


class EventAPI(APIv2):
    @classmethod
    def event(cls, event_key):
        event = Event.get_by_id(event_key)
        event_dict = ModelToDict.eventConverter(event)
        return json.dumps(event_dict, ensure_ascii=True)

    @classmethod
    def event_teams(cls, event_key):
        teams = Event.get_by_id(event_key).teams
        team_dicts = [ModelToDict.teamConverter(team) for team in teams]
        return json.dumps(team_dicts, ensure_ascii=True)

    @classmethod
    def event_matches(cls, event_key):
        matches = Event.get_by_id(event_key).matches
        match_dicts = [ModelToDict.matchConverter(match) for match in matches]
        return json.dumps(match_dicts, ensure_ascii=True)

    @classmethod
    def event_stats(cls, event_key):
        return json.dumps(Event.get_by_id(event_key).matchstats, ensure_ascii=True)

    @classmethod
    def event_rankings(cls, event_key):
        ranks = json.dumps(Event.get_by_id(event_key).rankings, ensure_ascii=True)
        if ranks is None or ranks == 'null':
            return '[]'
        else:
            return ranks

    @classmethod
    def event_awards(cls, event_key):
        awards = Event.get_by_id(event_key).awards
        award_dicts = [ModelToDict.awardConverter(award) for award in AwardHelper.organizeAwards(awards)]
        return json.dumps(award_dicts, ensure_ascii=True)

    @classmethod
    def event_district_points(cls, event_key):
        points = DistrictHelper.calculate_event_points(Event.get_by_id(event_key))
        return json.dumps(points, ensure_ascii=True)

    @classmethod
    def event_list(cls, year):
        event_keys = Event.query(Event.year == year).fetch(1000, keys_only=True)
        events = ndb.get_multi(event_keys)
        event_list = [ModelToDict.eventConverter(event) for event in events]
        return json.dumps(event_list, ensure_ascii=True)
