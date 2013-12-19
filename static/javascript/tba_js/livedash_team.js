/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  render: function() {
    fixLayout();
    var matches = [];
    if (this.state != null) {
      matches = this.state.event.matches;
    }
    return (
      <div className="row">
        <div className="col-sm-8">
          <WebcastCell />
        </div>
        <div className="col-sm-4">
          <MatchTable matches={matches} />
        </div>
      </div>
    );
  }
});

var WebcastCell = React.createClass({
  render: function() {
    return (
      <div id="webcast-container">
        <object type='application/x-shockwave-flash' height='100%' width='100%' id='live_embed_player_flash' data='http://www.twitch.tv/widgets/live_embed_player.swf?channel=tbagameday' bgcolor='#000000'><param name='allowFullScreen' value='true' /><param name='allowScriptAccess' value='always' /><param name='allowNetworking' value='all' /><param name='movie' value='http://www.twitch.tv/widgets/live_embed_player.swf' /><param name='flashvars' value='hostname=www.twitch.tv&channel={{webcast.channel}}&auto_play=true&start_volume=25&enable_javascript=true' /><param name='wmode' value='transparent' /></object>
      </div>
    );
  }
});

var MatchTable = React.createClass({
  render: function() {
    var matchRows = [];
    if (this.props.matches != null) {
      for (var i=0; i < this.props.matches.length; i++) {
        match = this.props.matches[i];
        matchRows.push(<MatchRowTop match={match} />);
        matchRows.push(<MatchRowBottom match={match} />);
      }
    }
    return (
      <div id="test">
        <table className="match-table">
          <thead>
            <tr className="key">
              <th rowSpan="2"><span className="glyphicon glyphicon-film"></span></th>
              <th rowSpan="2">Match</th>
              <th colSpan="3">Red Alliance</th>
              <th>Red Score</th>
            </tr>
            <tr className="key">
              <th colSpan="3">Blue Alliance</th>
              <th>Blue Score</th>
            </tr>
          </thead>
        </table>
        <div id="live-match-table-container">        
          <table id="test" className="match-table">
            <tbody>
              {matchRows}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
});

var MatchRowTop = React.createClass({
  render: function() {
    var name = this.props.match.name;
    var teams = this.props.match.alliances.red.teams.map(function (team) {
      return team.substring(3);
    });
    var score = this.props.match.alliances.red.score;
    return (
      <tr>
        <td rowSpan="2"><span className="glyphicon glyphicon-film"></span></td>
        <td rowSpan="2"><a href="/match/">{name}</a></td>
        <td className="red"><a href="/team/">{teams[0]}</a></td>
        <td className="red"><a href="/team/">{teams[1]}</a></td>
        <td className="red"><a href="/team/">{teams[2]}</a></td>
        <td className="redScore">{score}</td>
      </tr>
    );
  }
});

var MatchRowBottom = React.createClass({
  render: function() {
    var teams = this.props.match.alliances.blue.teams.map(function (team) {
      return team.substring(3);
    });
    var score = this.props.match.alliances.blue.score;
    return (
      <tr>
        <td className="blue"><a href="/team/">{teams[0]}</a></td>
        <td className="blue"><a href="/team/">{teams[1]}</a></td>
        <td className="blue"><a href="/team/">{teams[2]}</a></td>
        <td className="blueScore">{score}</td>
      </tr>
    );
  }
});

var a = React.renderComponent(
  <LivedashPanel />,
  document.getElementById('team-live-dash')
);

function test() {
  var newProps = {};
  $.ajax({
    dataType: 'json',
    url: '/_/livedash/2013casj',
    success: function(event) {
      event.matches.sort(function(match1, match2){return match1.order - match2.order});
      a.setState({event: event});
      setTimeout(test, 10000);
    }
  });
}

$( document ).ready(function() {
  test();

  $(window).resize(function(){
    fixLayout();
  });
});

function fixLayout() {
  var width = $("#webcast-container").width();
  var height = width * 9 / 16;
  $("#webcast-container").height(height);
//  $("#live-match-table").height(height);
}
