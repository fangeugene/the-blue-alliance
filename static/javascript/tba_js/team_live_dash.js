/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  render: function() {
    var teamMatches = [];
    var rankings = [];
    if (this.state != null) {
      rankings = this.state.event.rankings;
      
      var teamKey = $("#team-live-dash").attr('data-team-key-name');
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
        <div className="row">
          <div className="col-sm-4">
            <div className="row">
              <div className="col-xs-12">
                <RankBox rankings={rankings} />
              </div>
            </div>
            <div className="row">
              <div className="col-xs-12">
                <WLTBox teamMatches={teamMatches} />
              </div>
            </div>
          </div>
          <div className="col-sm-8">
            <MatchList teamMatches={teamMatches} />
          </div>
        </div>
      </div>
    );
  }
});

var MatchList = React.createClass({
  render: function() {
    var teamNum = $("#team-live-dash").attr('data-team-key-name').substring(3);

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
      var wlt;
      if ((alliance == 'red' && redScore > blueScore) || (alliance == 'blue' && blueScore > redScore)) {
        wlt = (<div className="wlt win">
                 <span>W</span>
               </div>);
      } else if ((alliance == 'red' && redScore < blueScore) || (alliance == 'blue' && blueScore < redScore)) {
        wlt = (<div className="wlt loss">
                 <span>L</span>
               </div>);
      } else {
        wlt = (<div className="wlt tie">
                 <span>T</span>
               </div>);
      }
      if (redScore == '?' || blueScore == '?') {
        wlt = (<div className="wlt">
                 <span>--</span>
               </div>);
      }
      matchRows.push(
        <div className="matchrow">
          <div className="num-time"><strong>{match.name}</strong><br />{matchTime}</div>
          <div className="alliances">
            <div className="red-alliance">{redAlliance}</div>
            <div className="blue-alliance">{blueAlliance}</div>
          </div>
          <div className="scores">
            <div className="red-score">{redScore}</div>
            <div className="blue-score">{blueScore}</div>
          </div>
          {wlt}
          <div className="clear-both"></div>
        </div>
      );
    }
    return (
      <div className="match-list well">
        {matchRows}
      </div>
    );
  }
});

var RankBox = React.createClass({
  render: function() {
    if (this.props.rankings == null) {
      return (
        <div className="well">
          No rankings available at this time.
        </div>
      )
    }
    var teamNum = $("#team-live-dash").attr('data-team-key-name').substring(3);
    var rank = "?";
    for (var i=0; i<this.props.rankings.length; i++) {
      if (this.props.rankings[i][1] == teamNum) {
        rank = this.props.rankings[i][0];
      }
    }
    return (
      <div className="well">
        Rank: {rank}
      </div>
    );
  }
});

var WLTBox = React.createClass({
  render: function() {
    var wins = 0;
    var losses = 0;
    var ties = 0;
    var teamKey = $("#team-live-dash").attr('data-team-key-name');
    for (var i=0; i<this.props.teamMatches.length; i++) {
      var match = this.props.teamMatches[i];
      var redTeams = match.alliances.red.teams;
      var redScore = match.alliances.red.score;
      var blueScore = match.alliances.blue.score;
      var onRed = redTeams.indexOf(teamKey) != -1;
      if (redScore == -1 || blueScore == -1){
        continue;
      } else if (redScore == blueScore) {
        ties += 1;
      } else if (redScore > blueScore) {
        if (onRed) {
          wins += 1;
        } else {
          losses += 1;
        }
      } else {
        if (onRed) {
          losses += 1;
        } else {
          wins += 1;
        }
      }
    }
    return (
      <div className="well">
        W-L-T: {wins}-{losses}-{ties}
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
