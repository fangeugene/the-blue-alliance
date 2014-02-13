import os
from google.appengine.ext import ndb
from template_engine import jinja2_engine
from consts.event_type import EventType
from controllers.base_controller import LoggedInHandler
from models.award import Award
from models.event import Event
from helpers.event_helper import EventHelper


class AdminMigration(LoggedInHandler):
  def get(self):
    self._require_admin()
    path = os.path.join(os.path.dirname(__file__), '../../templates/admin/migration.html')
    self.response.out.write(jinja2_engine.render(path, self.template_values))
