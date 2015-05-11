import collections
import json

# from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.runtime.apiproxy_errors import RequestTooLargeError

# from helpers.award_helper import AwardHelper
# from helpers.district_helper import DistrictHelper
# from helpers.model_to_dict import ModelToDict
from models.event import Event

from models.cached_query_result import CachedQueryResult
from helpers.model_json_converter import ModelJSONConverter


class EventQuery(object):
    @classmethod
    def event(cls, event_key):
        cache_key = 'event_v1:{}'.format(event_key)
        query = CachedQueryResult.get_by_id(cache_key)
        if query is None:
            print "MISSSSSS!!!!!"
            query_result = Event.get_by_id(event_key)
            if query_result is not None:
                CachedQueryResult(
                    id=cache_key,
                    result_json=json.dumps(ModelJSONConverter.to_json(query_result)),
                ).put()
        else:
            print "HIT!"
            query_result = query.result

        return query_result

    # @classmethod
    # def event_teams(cls, event_key):
    #     teams = Event.get_by_id(event_key).teams
    #     team_dicts = [ModelToDict.teamConverter(team) for team in teams]
    #     return json.dumps(team_dicts, ensure_ascii=True)

    # @classmethod
    # def event_matches(cls, event_key):
    #     matches = Event.get_by_id(event_key).matches
    #     match_dicts = [ModelToDict.matchConverter(match) for match in matches]
    #     return json.dumps(match_dicts, ensure_ascii=True)

    # @classmethod
    # def event_stats(cls, event_key):
    #     return json.dumps(Event.get_by_id(event_key).matchstats, ensure_ascii=True)

    # @classmethod
    # def event_rankings(cls, event_key):
    #     ranks = json.dumps(Event.get_by_id(event_key).rankings, ensure_ascii=True)
    #     if ranks is None or ranks == 'null':
    #         return '[]'
    #     else:
    #         return ranks

    # @classmethod
    # def event_awards(cls, event_key):
    #     awards = Event.get_by_id(event_key).awards
    #     award_dicts = [ModelToDict.awardConverter(award) for award in AwardHelper.organizeAwards(awards)]
    #     return json.dumps(award_dicts, ensure_ascii=True)

    # @classmethod
    # def event_district_points(cls, event_key):
    #     points = DistrictHelper.calculate_event_points(Event.get_by_id(event_key))
    #     return json.dumps(points, ensure_ascii=True)

    @classmethod
    def event_list(cls, year):
        cache_key = 'event_list_v1:{}'.format(year)
        query = CachedQueryResult.get_by_id(cache_key)
        if query is None:
            query_result = Event.query(Event.year == year).fetch()
            result_list = [ModelJSONConverter.to_json(r) for r in query_result]
            cls._put_list_helper(cache_key, result_list)
        else:
            query_result = []
            while True:
                query_result.extend(query.result)
                if query.additional_results is not None:
                    query = query.additional_results.get()
                else:
                    break

        return query_result

    @classmethod
    def _put_list_helper(cls, cache_key, result_list):
        """
        Splits up lists of models that are too large for a single
        CachedQueryResult into a linked list in the db.
        """
        bounds_queue = collections.deque()
        bounds_queue.append((0, len(result_list)))
        count = 0
        while len(bounds_queue) != 0:
            lower, upper = bounds_queue.popleft()

            try:
                if count == 0:
                    indexed_cache_key = cache_key
                else:
                    indexed_cache_key = '{}~{}'.format(cache_key, count)

                if len(bounds_queue) == 0:
                    additional_results = None
                else:
                    next_cache_key = '{}~{}'.format(cache_key, count + 1)
                    additional_results = ndb.Key(CachedQueryResult, next_cache_key)

                CachedQueryResult(
                    id=indexed_cache_key,
                    result_json=json.dumps(result_list[lower:upper]),
                    additional_results=additional_results,
                ).put()

                count += 1
            except RequestTooLargeError:
                mid = int((lower + upper) / 2)
                bounds_queue.appendleft((mid, upper))
                bounds_queue.appendleft((lower, mid))

