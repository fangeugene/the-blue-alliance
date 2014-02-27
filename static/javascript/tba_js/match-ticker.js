/** @jsx React.DOM */

var MatchTicker = React.createClass({
  render: function() {
    var followedTeamMatches = [];
    if (this.state != null && this.props != null) {
      // Combine matches from all events
      for (eventKey in this.state) {
        for (var i=0; i<this.state[eventKey].matches.length; i++) {
          var match = this.state[eventKey].matches[i];
          
          // Only show matches with times
          if (match.utc == null) {
            continue;
          }
          
          // Only show matches of followed teams
          var matchTeamKeys = match.alliances.red.teams.concat(match.alliances.blue.teams);
          for (var j=0; j<matchTeamKeys.length; j++) {
            if (this.props.followedTeams[matchTeamKeys[j]]) {
              // Add event key to match object
              match.event_key = eventKey.substring(4).toUpperCase();
              followedTeamMatches.push(match);
              break;
            }
          }
        }
      }
      
      // Sort by time
      followedTeamMatches.sort(function(match1, match2){return Date.parse(match1.utc) - Date.parse(match2.utc)});
    }
    return (
      <div>
        <MatchList followedTeamMatches={followedTeamMatches} followedTeams={this.props.followedTeams} />
      </div>
    );
  }
});

var MatchList = React.createClass({
  render: function() {
    var headerRow = [<th>Match</th>, <th>Red Alliance</th>, <th>Blue Alliance</th>, <th>Result</th>];
    var matchTableHeader = <tr>{headerRow}</tr>;

    var matchRows = [];
    var flag = false;
    for (var i=0; i<this.props.followedTeamMatches.length; i++) {
      var match = this.props.followedTeamMatches[i];
      var redTeams = match.alliances.red.teams.map(function (team) {
        return team.substring(3);
      });
      var blueTeams = match.alliances.blue.teams.map(function (team) {
        return team.substring(3);
      });
      var redScore = match.alliances.red.score == -1 ? '?' : match.alliances.red.score;
      var blueScore = match.alliances.blue.score == -1 ? '?' : match.alliances.blue.score;
      if (!flag && (match.alliances.red.score == -1 || match.alliances.blue.score == -1)){
        var nextMatch = this.props.followedTeamMatches[i+1];
        var nextMatchSeconds = Math.floor((Date.parse(nextMatch.utc) - new Date()) / 1000);
        if (nextMatchSeconds > 0) {
          var nextMatchMinutes = Math.floor(nextMatchSeconds / 60);
          nextMatchSeconds %= 60;
          matchRows.push(<div id="next-matchrow">Next match in <strong>{nextMatchMinutes} min {nextMatchSeconds} sec</strong></div>);
        } else {
          matchRows.push(<div id="current-matchrow">Current match</div>);
        }
        flag = true;
      }
      var redAlliance = [];
      for (var j=0; j<redTeams.length; j++) {
        var team = redTeams[j];
        if (this.props.followedTeams['frc' + team]) {
          redAlliance.push(<div className="team team-highlight">{team}</div>);
        } else {
          redAlliance.push(<div className="team">{team}</div>)
        }
      }
      var blueAlliance = [];
      for (var j=0; j<blueTeams.length; j++) {
        var team = blueTeams[j];
        if (this.props.followedTeams['frc' + team]) {
          blueAlliance.push(<div className="team team-highlight">{team}</div>);
        } else {
          blueAlliance.push(<div className="team">{team}</div>)
        }
      }
      redAlliance.push(<div className="clear-both"></div>);
      blueAlliance.push(<div className="clear-both"></div>);
      var matchTime = new Date(match.utc);  // Converts UTC to local time
      var hour24 = matchTime.getHours();
      var hour12 = (hour24 % 12);
      if (hour12 == 0) {
        hour12 = 12;
      }
      var minute = matchTime.getMinutes();
      var matchTimeStr = hour12 + ':' + ((''+minute).length<2 ? '0' :'')+minute;
      matchTimeStr += hour24 < 12 ? ' AM' : ' PM';
      var eventMatchName = match.event_key + ' ' + match.name
      matchRows.push(
        <div className="matchrow">
          <div className="num-time"><strong>{eventMatchName}</strong><br />{matchTimeStr}</div>
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
  <MatchTicker />,
  document.getElementById('match-ticker')
);

function updateMatches() {
  var eventKeys = JSON.parse($("#match-ticker").attr('data-event-key-names'));
  eventKeys.forEach(function (eventKey) {
    $.ajax({
      dataType: 'json',
      url: '/_/live-event/' + eventKey + '/0', // TODO: replace with timestamp
      success: function(event) {
        var newState = {}
        newState[eventKey] = event;
        a.setState(newState);
//        fixLayout();
      }
    });
  });
}

$(document).ready(function() {
  // Set up following list
  var followedTeamList = JSON.parse($("#match-ticker").attr('data-team-key-names'));
  var followedTeams = {}
  for (var i=0; i<followedTeamList.length; i++) {
    followedTeams[followedTeamList[i]] = true;
  }
  a.setProps({followedTeams: followedTeams});
  
  // Start match updating
  updateMatches();
  setInterval(updateMatches, 10000)
  
  // Periodically update countdown
  setInterval(function() {a.setState()}, 1000);

//  $(window).resize(function(){
//    fixLayout();
//  });
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
