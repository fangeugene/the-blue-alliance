import datetime
import os
import logging

from google.appengine.ext import ndb
from common import template

from controllers.base_controller import LoggedInHandler
from helpers.event.event_webcast_adder import EventWebcastAdder
from helpers.memcache.memcache_webcast_flusher import MemcacheWebcastFlusher


from models.event import Event
from models.suggestion import Suggestion


class AdminEventWebcastSuggestionsReviewController(LoggedInHandler):
    """
    View the list of suggestions.
    """
    def get(self):
        self._require_admin()

        suggestions = Suggestion.query().filter(
            Suggestion.review_state == Suggestion.REVIEW_PENDING).filter(
            Suggestion.target_model == "event")

        self.template_values.update({
            "event_key": self.request.get("event_key"),
            "success": self.request.get("success"),
            "suggestions": suggestions,
        })

        path = os.path.join(os.path.dirname(__file__), '../../../templates/admin/event_webcast_suggestion_list.html')
        self.response.out.write(template.render(path, self.template_values))

    def post(self):
        self._require_admin()

        if self.request.get("verdict") == "accept":
            webcast = dict()
            webcast["type"] = self.request.get("webcast_type")
            webcast["channel"] = self.request.get("webcast_channel")
            if self.request.get("webcast_file"):
                webcast["file"] = self.request.get("webcast_file")

            event = Event.get_by_id(self.request.get("event_key"))
            suggestion = Suggestion.get_by_id(int(self.request.get("suggestion_key")))

            EventWebcastAdder.add_webcast(event, webcast)
            MemcacheWebcastFlusher.flush()

            suggestion.review_state = Suggestion.REVIEW_ACCEPTED
            suggestion.reviewer = self.user_bundle.account.key
            suggestion.reviewer_at = datetime.datetime.now()
            suggestion.put()

            self.redirect("/admin/suggestions/event/webcast/review?success=accept&event_key=%s" % event.key.id())
            return

        elif self.request.get("verdict") == "reject":
            suggestion = Suggestion.get_by_id(int(self.request.get("suggestion_key")))

            suggestion.review_state = Suggestion.REVIEW_REJECTED
            suggestion.reviewer = self.user_bundle.account.key
            suggestion.reviewer_at = datetime.datetime.now()
            suggestion.put()

            self.redirect("/admin/suggestions/event/webcast/review?success=reject")
            return

        self.redirect("/admin/suggestions/event/webcast/review")



