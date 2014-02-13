import os
import logging
import datetime
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb
from template_engine import jinja2_engine

import tba_config

from base_controller import CacheableHandler
from helpers.event_helper import EventHelper

from models.event import Event
from models.insight import Insight
from models.team import Team
from models.sitevar import Sitevar


def render_static(page):
    memcache_key = "main_%s" % page
    html = memcache.get(memcache_key)

    if html is None:
        html = jinja2_engine.render('{}.html'.format(page), {})
        if tba_config.CONFIG["memcache"]:
            memcache.set(memcache_key, html, 86400)

    return html


class MainKickoffHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_kickoff"
        self._cache_version = 3

    def _render(self, *args, **kw):
        kickoff_datetime_est = datetime.datetime(2014, 1, 4, 10, 30)
        kickoff_datetime_utc = kickoff_datetime_est + datetime.timedelta(hours=5)

        is_kickoff = datetime.datetime.now() >= kickoff_datetime_est - datetime.timedelta(days=1)  # turn on 1 day before

        return jinja2_engine.render('index_kickoff.html', {'is_kickoff': is_kickoff,
                                                      'kickoff_datetime_est': kickoff_datetime_est,
                                                      'kickoff_datetime_utc': kickoff_datetime_utc,
                                                      })


class MainBuildseasonHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_buildseason"
        self._cache_version = 1

    def _render(self, *args, **kw):
        endbuild_datetime_est = datetime.datetime(2014, 2, 18, 0, 0)
        endbuild_datetime_utc = endbuild_datetime_est + datetime.timedelta(hours=5)

        return jinja2_engine.render('index_buildseason.html', {'endbuild_datetime_est': endbuild_datetime_est,
                                                          'endbuild_datetime_utc': endbuild_datetime_utc
                                                          })


class MainCompetitionseasonHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60
        self._cache_key = "main_competitionseason"
        self._cache_version = 5

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        return jinja2_engine.render('index_competitionseason.html', template_values)


class MainInsightsHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_insights"
        self._cache_version = 1

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        insights = ndb.get_multi([ndb.Key(Insight, Insight.renderKeyName(2013, insight_name)) for insight_name in Insight.INSIGHT_NAMES.values()])
        for insight in insights:
            if insight:
                template_values[insight.name] = insight

        return jinja2_engine.render('index_insights.html', template_values)


class MainOffseasonHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "main_offseason"
        self._cache_version = 2

    def _render(self, *args, **kw):
        week_events = EventHelper.getWeekEvents()
        template_values = {
            "events": week_events,
        }

        return jinja2_engine.render('index_offseason.html', template_values)


class ContactHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_contact"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('contact.html', {})


class HashtagsHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_hashtags"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('hashtags.html', {})


class AboutHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_about"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('about.html', {})


class ThanksHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_thanks"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('thanks.html', {})


class OprHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_opr"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('opr.html', {})


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        try:
            q = self.request.get("q")
            logging.info("search query: %s" % q)
            if q.isdigit():
                team_id = "frc%s" % q
                team = Team.get_by_id(team_id)
                if team:
                    self.redirect(team.details_url)
                    return None
        except Exception, e:
            logging.warning("warning: %s" % e)
        finally:
            self.response.out.write(render_static("search"))


class GamedayHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_gameday"
        self._cache_version = 1

    def _render(self, *args, **kw):
        special_webcasts_future = Sitevar.get_by_id_async('gameday.special_webcasts')
        special_webcasts_temp = special_webcasts_future.get_result()
        if special_webcasts_temp:
            special_webcasts_temp = special_webcasts_temp.contents
        else:
            special_webcasts_temp = {}
        special_webcasts = []
        for webcast in special_webcasts_temp.values():
            toAppend = {}
            for key, value in webcast.items():
                toAppend[str(key)] = str(value)
            special_webcasts.append(toAppend)

        ongoing_events = []
        ongoing_events_w_webcasts = []
        week_events = EventHelper.getWeekEvents()
        for event in week_events:
            if event.within_a_day:
                ongoing_events.append(event)
                if event.webcast:
                    valid = []
                    for webcast in event.webcast:
                        if 'type' in webcast and 'channel' in webcast:
                            event_webcast = {'event': event}
                            valid.append(event_webcast)
                    # Add webcast numbers if more than one for an event
                    if len(valid) > 1:
                        count = 1
                        for event in valid:
                            event['count'] = count
                            count += 1
                    ongoing_events_w_webcasts += valid

        template_values = {'special_webcasts': special_webcasts,
                           'ongoing_events': ongoing_events,
                           'ongoing_events_w_webcasts': ongoing_events_w_webcasts}

        return jinja2_engine.render('gameday.html', template_values)


class PageNotFoundHandler(webapp2.RequestHandler):
    def get(self, *args):
        self.error(404)
        self.response.out.write(render_static("404"))


class WebcastsHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_webcasts"
        self._cache_version = 2

    def _render(self, *args, **kw):
        event_keys = Event.query(Event.year == 2014).order(Event.start_date).fetch(500, keys_only=True)
        events = ndb.get_multi(event_keys)

        template_values = {
            'events': events,
        }

        return jinja2_engine.render('webcasts.html', template_values)


class RecordHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_record"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('record.html', {})


class ApiDocumentationHandler(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "api_docs"
        self._cache_version = 1

    def _render(self, *args, **kw):
        return jinja2_engine.render('apidocs.html', {})
