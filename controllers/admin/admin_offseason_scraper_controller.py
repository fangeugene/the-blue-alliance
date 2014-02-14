from datetime import datetime
import logging
import os

from google.appengine.ext import ndb
from template_engine import jinja2_engine

from controllers.base_controller import LoggedInHandler
from datafeeds.datafeed_usfirst_offseason import DatafeedUsfirstOffseason

from consts.event_type import EventType
from helpers.event_manipulator import EventManipulator
from models.event import Event


class AdminOffseasonScraperController(LoggedInHandler):
    """
    View and add un-added offseasons from FIRST's site
    """
    def get(self):
        self._require_admin()

        df = DatafeedUsfirstOffseason()
        new_events = df.getEventList()
        old_events = Event.query().filter(
            Event.event_type_enum == EventType.OFFSEASON).filter(
            Event.year == 2013).filter(
            Event.first_eid != None).fetch(100)

        old_first_eids = [event.first_eid for event in old_events]
        truly_new_events = [event for event in new_events if event.first_eid not in old_first_eids]

        self.template_values.update({
            "events": truly_new_events,
            "event_key": self.request.get("event_key"),
            "success": self.request.get("success"),

        })

        self.response.out.write(jinja2_engine.render('admin/offseasons.html', self.template_values))

    def post(self):
        self._require_admin()

        if self.request.get("submit") == "duplicate":
            old_event = Event.get_by_id(self.request.get("duplicate_event_key"))
            old_event.first_eid = self.request.get("event_first_eid")
            old_event.put()

            self.redirect("/admin/offseasons?success=duplicate&event_key=%s" % self.request.get("duplicate_event_key"))
            return

        if self.request.get("submit") == "create":

            start_date = None
            if self.request.get("event_start_date"):
                start_date = datetime.strptime(self.request.get("event_start_date"), "%Y-%m-%d")

            end_date = None
            if self.request.get("event_end_date"):
                end_date = datetime.strptime(self.request.get("event_end_date"), "%Y-%m-%d")

            event_key = str(self.request.get("event_year")) + str.lower(str(self.request.get("event_short")))

            event = Event(
                id=event_key,
                event_type_enum=int(self.request.get("event_type_enum")),
                event_short=self.request.get("event_short"),
                first_eid=self.request.get("event_first_eid"),
                name=self.request.get("event_name"),
                year=2013, #TODO: don't hardcode me -gregmarra 20130921
                start_date=start_date,
                end_date=end_date,
                location=self.request.get("event_location"),
                )
            event = EventManipulator.createOrUpdate(event)

            self.redirect("/admin/offseasons?success=create&event_key=%s" % event_key)
            return

        self.redirect("/admin/offseasons")
