import os

from template_engine import jinja2_engine

from base_controller import CacheableHandler

from helpers.event_helper import EventHelper


class Gameday2Controller(CacheableHandler):
    def __init__(self, *args, **kw):
        super(CacheableHandler, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24 * 7
        self._cache_key = "main_gameday2"
        self._cache_version = 1

    def _render(self, *args, **kw):
        events = EventHelper.getWeekEvents()

        webcasts = []
        for event in events:
            webcasts.append({
                "key": event.key_name,
                "name": event.name,
                "webcast": event.webcast,
                })

        template_values = {'webcasts': webcasts}

        return jinja2_engine.render('gameday2.html', template_values)
