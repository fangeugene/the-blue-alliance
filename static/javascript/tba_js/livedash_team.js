/** @jsx React.DOM */

var LivedashPanel = React.createClass({
  render: function() {
    var matches = [];
    if (this.state != null) {
      matches = this.state.event.matches;
    }
    return (
      <div className="panel panel-default">
        <div className="panel-heading">
          Currently competing at
        </div>
        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <WebcastCell />
            </div>
            <div className="col-sm-4">
              <MatchTable matches={matches} />
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

var a = React.renderComponent(
  <LivedashPanel />,
  document.getElementById('team-live-dash')
);

function test() {
  var newProps = {};
  $.ajax({
    dataType: 'json',
    url: '/_/livedash/event/2013testpresent',
    success: function(event) {
      a.setState({event: event});
      setTimeout(test, 1000);
    }
  });
}

$( document ).ready(function() {
  test();
});
