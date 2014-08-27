import json
import logging
import webapp2

from datetime import datetime
from google.appengine.ext import ndb

from api.v2.event_api import EventAPI

from controllers.api.api_base_controller import ApiBaseController

from helpers.award_helper import AwardHelper
from helpers.district_helper import DistrictHelper
from helpers.model_to_dict import ModelToDict

from models.event import Event


class ApiEventController(ApiBaseController):
    CACHE_KEY_FORMAT = "apiv2_event_controller_{}"  # (event_key)
    CACHE_VERSION = 2
    CACHE_HEADER_LENGTH = 60 * 60

    def __init__(self, *args, **kw):
        super(ApiEventController, self).__init__(*args, **kw)
        self.event_key = self.request.route_kwargs["event_key"]
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    @property
    def _validators(self):
        return [("event_id_validator", self.event_key)]

    def _check_event_exists(self, event_key):
        if Event.get_by_id(event_key) is None:
            self._errors = json.dumps({"404": "%s event not found" % self.event_key})
            self.abort(404)

    def _track_call(self, event_key):
        self._track_call_defer('event', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event(event_key)


class ApiEventTeamsController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_teams_controller_{}"  # (event_key)
    CACHE_VERSION = 1
    CACHE_HEADER_LENGTH = 60 * 60

    def __init__(self, *args, **kw):
        super(ApiEventTeamsController, self).__init__(*args, **kw)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/teams', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_teams(event_key)


class ApiEventMatchesController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_matches_controller_{}"  # (event_key)
    CACHE_VERSION = 1
    CACHE_HEADER_LENGTH = 61

    def __init__(self, *args, **kw):
        super(ApiEventMatchesController, self).__init__(*args, **kw)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/matches', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_matches(event_key)


class ApiEventStatsController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_stats_controller_{}"  # (event_key)
    CACHE_VERSION = 0
    CACHE_HEADER_LENGTH = 61

    def __init__(self, *args, **kw):
        super(ApiEventStatsController, self).__init__(*args, **kw)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/stats', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_stats(event_key)


class ApiEventRankingsController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_rankings_controller_{}"  # (event_key)
    CACHE_VERSION = 0
    CACHE_HEADER_LENGTH = 61

    def __init__(self, *args, **kw):
        super(ApiEventRankingsController, self).__init__(*args, **kw)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/rankings', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_rankings(event_key)


class ApiEventAwardsController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_awards_controller_{}"  # (event_key)
    CACHE_VERSION = 3
    CACHE_HEADER_LENGTH = 61

    def __init__(self, *args, **kw):
        super(ApiEventAwardsController, self).__init__(*args, **kw)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/awards', event_key)

    def _render(self,event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_awards(event_key)


class ApiEventDistrictPointsController(ApiEventController):
    CACHE_KEY_FORMAT = "apiv2_event_district_points_controller_{}"  # (event_key)
    CACHE_VERSION = 0
    CACHE_HEADER_LENGTH = 61

    def __init__(self, *args, **kw):
        super(ApiEventDistrictPointsController, self).__init__(*args, **kw)
        self.partial_cache_key = self.CACHE_KEY_FORMAT.format(self.event_key)

    def _track_call(self, event_key):
        self._track_call_defer('event/district_points', event_key)

    def _render(self, event_key):
        self._check_event_exists(event_key)
        return EventAPI.event_district_points(event_key)


class ApiEventListController(ApiBaseController):
    CACHE_KEY_FORMAT = "apiv2_event_list_controller_{}"  # (year)
    CACHE_VERSION = 2
    CACHE_HEADER_LENGTH = 60 * 60 * 24

    def __init__(self, *args, **kw):
        super(ApiEventListController, self).__init__(*args, **kw)
        self.year = int(self.request.route_kwargs.get("year") or datetime.now().year)
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.year)

    @property
    def _validators(self):
        return []

    def _track_call(self, *args, **kw):
        self._track_call_defer('event/list', self.year)

    def _render(self, year=None):
        if self.year < 1992 or self.year > datetime.now().year + 1:
            self._errors = json.dumps({"404": "No events found for %s" % self.year})
            self.abort(404)

        return EventAPI.event_list(self.year)
