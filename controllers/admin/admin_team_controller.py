import os

from template_engine import jinja2_engine

from controllers.base_controller import LoggedInHandler
from models.event_team import EventTeam
from models.team import Team


class AdminTeamList(LoggedInHandler):
    """
    The view of a list of teams.
    """
    def get(self):
        self._require_admin()

        teams = Team.query().order(Team.team_number)

        self.template_values.update({
            "teams": teams,
        })

        self.response.out.write(jinja2_engine.render('admin/team_list.html', self.template_values))


class AdminTeamDetail(LoggedInHandler):
    """
    The view of a single Team.
    """
    def get(self, team_number):
        self._require_admin()

        team = Team.get_by_id("frc" + team_number)
        event_teams = EventTeam.query(EventTeam.team == team.key).fetch(500)

        self.template_values.update({
            'event_teams': event_teams,
            'team': team,
        })

        self.response.out.write(jinja2_engine.render('admin/team_details.html', self.template_values))
