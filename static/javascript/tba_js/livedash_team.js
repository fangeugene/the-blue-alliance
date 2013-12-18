/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  getInitialState: function() {
    return {event: []};
  },
  updateEventFromServer: function() {
    $.ajax({
      dataType: "json",
      url: "/api/v1/event/details?event=" + this.props.eventKeyName,
      success: function(event) {
        event.url = "/event/" + event.key;
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
              <MatchTable matches={this.state.event.matches} />
            </div>
          </div>
          <div className="row">
            <div className="col-sm-8">
              <WebcastCell />
            </div>
            <div className="col-sm-4">
            <MatchTable matches={this.state.event.matches} />
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
    var matches = [];
    if (this.props.matches != null) {
      matches = this.props.matches
    }
    var matchRows = matches.map(function (match) {
      return <MatchRow match={match} />;
    });
    return (
      <div className="well">
        {matchRows}
      </div>
    );
  }
});

var MatchRow = React.createClass({
  render: function() {
    return (
      <div>
        {this.props.match}
      </div>
    );
  }
});

React.renderComponent(
  <LivedashPanel eventKeyName={document.getElementById('team-live-dash').getAttribute('data-event-key-name')}/>,
  document.getElementById('team-live-dash')
);
