/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  getInitialState: function() {
    return {event: []};
  },
  updateEventFromServer: function() {
    $.ajax({
      dataType: "json",
      url: "/_/livedash/event/" + this.props.eventKeyName,
      success: function(event) {
        event.url = "/event/" + this.props.eventKeyName;
        this.setState({event: event});
      }.bind(this)
    });
  },
  componentWillMount: function() {
    this.updateEventFromServer();
//    setInterval(this.updateEventFromServer, 1000);
  },
  render: function() {
    return (
      <div className="panel panel-default">
        <div className="panel-heading">
          Currently competing at <a href={this.state.event.url}><strong>{this.state.event.name}</strong></a>
        </div>
        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <WebcastCell />
            </div>
            <div className="col-sm-4">
              <MatchTable matchKeys={this.state.event.match_keys} />
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
      <div className="well">
        WEBCAST GOES HERE
      </div>
    );
  }
});

var MatchTable = React.createClass({
  render: function() {
    var matchKeys = [];
    if (this.props.matchKeys != null) {
      matchKeys = this.props.matchKeys
    }
    var matchRows = matchKeys.map(function (matchKey) {
      return <MatchRow matchKey={matchKey} />;
    });
    return (
      <div className="well">
        {matchRows}
      </div>
    );
  }
});

var MatchRow = React.createClass({
  getInitialState: function() {
    return {match: []};
  },
  updateMatchFromServer: function() {
    $.ajax({
      dataType: "json",
      url: "/_/livedash/match/" + this.props.matchKey,
      success: function(match) {
        this.setState({match: match});
      }.bind(this)
    });
  },
  componentWillMount: function() {
    this.updateMatchFromServer();
//    setInterval(this.updateEventFromServer, 1000);
  },
  render: function() {
    return (
      <div>
        {this.state.match}
      </div>
    );
  }
});

React.renderComponent(
  <LivedashPanel eventKeyName={document.getElementById('team-live-dash').getAttribute('data-event-key-name')}/>,
  document.getElementById('team-live-dash')
);
