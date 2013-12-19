/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  render: function() {
    fixLayout();
    var matches = [];
    if (this.state != null) {
      matches = this.state.event.matches;
    }
    return (
      <div>
        <div className="row">
          <div className="col-sm-8">
            <WebcastCell />
          </div>
          <div className="col-sm-4">
            <MatchList matches={matches} />
          </div>
        </div>
        <div className="row">
          <div className="col-sm-8">
            <div className="row">
              <div className="col-sm-4">
                <div className="well">1</div>
              </div>
              <div className="col-sm-4">
                <div className="well">1</div>
              </div>
              <div className="col-sm-4">
                <div className="well">1</div>
              </div>
            </div>
          </div>
          <div className="col-sm-4">
            <div className="row">
              <div className="col-sm-6">
                <div className="well">Rank</div>
              </div>
              <div className="col-sm-6">
                <div className="well">W-L-T</div>
              </div>
            </div>
          </div>
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

var MatchList = React.createClass({
  render: function() {
    var matchRows = [];
    var flag = false;
    
    var teamMatches = [];
    var teamKey = $("#team-live-dash").attr('data-team-key-name');
    for (var i=0; i<this.props.matches.length; i++) {
      var match = this.props.matches[i];
      var matchTeamKeys = match.alliances.red.teams.concat(match.alliances.blue.teams);
      for (var j=0; j<matchTeamKeys.length; j++) {
        if (teamKey == matchTeamKeys[j]) {
          teamMatches.push(match);
          break;
        }
      }
    }
    
    if (teamMatches != null) {
      for (var i=0; i<teamMatches.length; i++) {
        var match = teamMatches[i];
        if (!flag && (match.alliances.red.score == -1 || match.alliances.blue.score == -1)){
          matchRows.push(<NextMatchRow />);
          flag = true;
        }
        matchRows.push(<MatchRow match={match} />);
      }
    }
    return (
      <div id="test" className="well">
        {matchRows}
      </div>
    );
  }
});

var MatchRow = React.createClass({
  render: function() {
    var name = this.props.match.name;
    var redTeams = this.props.match.alliances.red.teams.map(function (team) {
      return team.substring(3);
    });
    var blueTeams = this.props.match.alliances.blue.teams.map(function (team) {
      return team.substring(3);
    });
    var redScore = this.props.match.alliances.red.score;
    var blueScore = this.props.match.alliances.blue.score;
    if (redScore == -1) {
      redScore = '?';
    }
    if (blueScore == -1) {
      blueScore = '?';
    }
    return (
      <div className="match">
        <div className="match-number">{name}</div>
        <div className="alliances">
          <div className="red">{redTeams[0]}, {redTeams[1]}, {redTeams[2]} - {redScore}</div>
          <div className="blue">{blueTeams[0]}, {blueTeams[1]}, {blueTeams[2]} - {blueScore}</div>
        </div>
      </div>
    );
  }
});

var NextMatchRow = React.createClass({
  render: function() {
    return (
      <div id="next-match">
        Next match in 3:13
      </div>
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
    url: '/_/livedash/' + $("#team-live-dash").attr('data-event-key-name'),
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
  $("#test").height(height);
  
  var $parentDiv = $("#test");
  var $innerListItem = $("#next-match");
  if ($parentDiv && $innerListItem.position()) {
    $parentDiv.animate({
      scrollTop: $parentDiv.scrollTop() + $innerListItem.position().top - $parentDiv.height()/2 + $innerListItem.height()/2
    }, 250);
  }
}
