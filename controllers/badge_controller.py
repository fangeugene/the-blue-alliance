import os
import urllib2
import StringIO
import datetime

from PIL import Image, ImageDraw, ImageFont


from base_controller import CacheableHandler
from consts.event_type import EventType
from helpers.event_helper import EventHelper
from helpers.data_fetchers.team_details_data_fetcher import TeamDetailsDataFetcher

from models.team import Team


class TeamBadge(CacheableHandler):
    """
    """
    def __init__(self, *args, **kw):
        super(TeamBadge, self).__init__(*args, **kw)
        self._cache_expiration = 60 * 60 * 24
        self._cache_key = "team_badge:{}"
        self._cache_version = 1

    def get(self, team_num):
        team_num = urllib2.unquote(team_num)
        self._cache_key = self._cache_key.format(team_num)
        super(TeamBadge, self).get(team_num)

    def _render(self, team_num):
#         self.response.headers['Cache-Control'] = 'public, max-age=%d' % self._cache_expiration
#         self.response.headers['Pragma'] = 'Public'
        self.response.headers['content-type'] = 'image/png'

        team = Team.get_by_id('frc{}'.format(team_num))
        if team is None:
            return None

        year = datetime.datetime.now().year
        events_sorted, matches_by_event_key, _, _ = TeamDetailsDataFetcher.fetch(team, year, return_valid_years=False)

        badge_background_path = os.path.join(os.path.dirname(__file__), '../static/images/tba_badge_background.png')
        image = Image.open(badge_background_path)
        width, height = image.size

        draw = ImageDraw.Draw(image)
        font_path = os.path.join(os.path.dirname(__file__), '../utils/fonts/tahoma.ttf')
        boldfont_path = os.path.join(os.path.dirname(__file__), '../utils/fonts/tahomabd.ttf')
        teamname_font = ImageFont.truetype(boldfont_path, 16)
        event_font = ImageFont.truetype(font_path, 10)

        team_str = "Team {}".format(team.team_number)
        if team.nickname is not None:
            team_str += " - {}".format(team.nickname)

        draw.text((10, 2), team_str, (0, 0, 0), font=teamname_font)

        STARTING_TOP_OFFSET = 22
        top_offset = STARTING_TOP_OFFSET
        left_offset = 15
        for event in events_sorted:
            if not event.official:
                continue
            event_matches = matches_by_event_key.get(event.key, [])
            wlt_str = ''
            if event_matches:
                wlt = EventHelper.calculateTeamWLTFromMatches(team.key_name, event_matches)
                wlt_str = ' ({}-{}-{})'.format(wlt['win'], wlt['loss'], wlt['tie'])
            event_date = event.start_date.strftime('%b %d')
            event_name = event.name
            if event.short_name:
                event_name = '{} {}'.format(event.short_name, EventType.type_names_short[event.event_type_enum])
            event_str = "{}: {}{}".format(event_date, event_name, wlt_str)
            draw.text((left_offset, top_offset), event_str, (0, 0, 0), font=event_font)
            top_offset += 10
            if top_offset > height - 10:
                top_offset = STARTING_TOP_OFFSET
                left_offset = width / 2

        output = StringIO.StringIO()
        image.save(output, format="png")
        return output.getvalue()
