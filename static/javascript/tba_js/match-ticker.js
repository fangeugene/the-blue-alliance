/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  render: function() {
    var teamMatches = [];
    var rankings = [];
    if (this.state != null) {
      rankings = this.state.event.rankings;
      
      var teamKey = $("#match-ticker").attr('data-team-key-name');
      for (var i=0; i<this.state.event.matches.length; i++) {
        var match = this.state.event.matches[i];
        var matchTeamKeys = match.alliances.red.teams.concat(match.alliances.blue.teams);
        for (var j=0; j<matchTeamKeys.length; j++) {
          if (teamKey == matchTeamKeys[j]) {
            teamMatches.push(match);
            break;
          }
        }
      }
    }
    return (
      <div>
        <MatchList teamMatches={teamMatches} />
      </div>
    );
  }
});

var MatchList = React.createClass({
  render: function() {
    var teamNum = $("#match-ticker").attr('data-team-key-name').substring(3);

    var headerRow = [<th>Match</th>, <th>Red Alliance</th>, <th>Blue Alliance</th>, <th>Result</th>];
    var matchTableHeader = <tr>{headerRow}</tr>;

    var matchRows = [];
    var flag = false;
    for (var i=0; i<this.props.teamMatches.length; i++) {
      var match = this.props.teamMatches[i];
      var alliance;
      var redTeams = match.alliances.red.teams.map(function (team) {
        var s = team.substring(3);
        if (s == teamNum) {
          alliance = 'red';
        }
        return s;
      });
      var blueTeams = match.alliances.blue.teams.map(function (team) {
        var s = team.substring(3);
        if (s == teamNum) {
          alliance = 'blue';
        }
        return s;
      });
      var redScore = match.alliances.red.score == -1 ? '?' : match.alliances.red.score;
      var blueScore = match.alliances.blue.score == -1 ? '?' : match.alliances.blue.score;
      if (!flag && (match.alliances.red.score == -1 || match.alliances.blue.score == -1)){
        matchRows.push(<div id="next-matchrow">Next match in 6:04</div>);
        flag = true;
      }
      var redAlliance = [];
      for (var j=0; j<redTeams.length; j++) {
        var team = redTeams[j];
        if (team == teamNum) {
          redAlliance.push(<div className="team team-highlight">{team}</div>);
        } else {
          redAlliance.push(<div className="team">{team}</div>)
        }
      }
      var blueAlliance = [];
      for (var j=0; j<blueTeams.length; j++) {
        var team = blueTeams[j];
        if (team == teamNum) {
          blueAlliance.push(<div className="team team-highlight">{team}</div>);
        } else {
          blueAlliance.push(<div className="team">{team}</div>)
        }
      }
      redAlliance.push(<div className="clear-both"></div>);
      blueAlliance.push(<div className="clear-both"></div>);
      var matchTime = match.time_str == null ? '--' : match.time_str;
      matchRows.push(
        <div className="matchrow">
          <div className="num-time"><strong>CASJ {match.name}</strong><br />{matchTime}</div>
          <div className="alliances">
            <div className="red-alliance">{redAlliance}</div>
            <div className="blue-alliance">{blueAlliance}</div>
          </div>
          <div className="scores">
            <div className="red-score">{redScore}</div>
            <div className="blue-score">{blueScore}</div>
          </div>
          <div className="clear-both"></div>
        </div>
      );
    }
    return (
      <div className="match-list">
        {matchRows}
      </div>
    );
  }
});

var a = React.renderComponent(
  <LivedashPanel />,
  document.getElementById('match-ticker')
);

function test() {
  var newProps = {};
  $.ajax({
    dataType: 'json',
    url: '/_/live-event/' + $("#match-ticker").attr('data-event-key-name') + '/0', // TODO: replace with timestamp
    success: function(event) {
      event.matches.sort(function(match1, match2){return match1.order - match2.order});
      a.setState({event: event});
      fixLayout();
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
  var $parentDiv = $(".match-list");
  var $innerListItem = $("#next-matchrow");
  if ($parentDiv && $innerListItem.position()) {
    $parentDiv.animate({
      scrollTop: $parentDiv.scrollTop() + $innerListItem.position().top - $parentDiv.height()/2 + $innerListItem.height()/2
    }, 250);
  }
}
