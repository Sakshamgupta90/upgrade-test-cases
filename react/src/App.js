import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';

function Greeting({ name }) {
  return <h2>Hello, {name}</h2>;
}

Greeting.propTypes = { name: PropTypes.string };
Greeting.defaultProps = { name: 'stranger' };

class SearchBox extends React.Component {
  state = { query: '' };

  componentWillMount() {
    this.setState({ query: this.props.initialQuery || '' });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.initialQuery !== this.props.initialQuery) {
      this.setState({ query: nextProps.initialQuery });
    }
  }

  componentDidMount() {
    ReactDOM.findDOMNode(this.refs.input).focus();
  }

  render() {
    return (
      <input
        ref="input"
        value={this.state.query}
        onChange={(e) => this.setState({ query: e.target.value })}
      />
    );
  }
}

SearchBox.propTypes = { initialQuery: PropTypes.string };

export default class App extends React.Component {
  render() {
    return (
      <div>
        <Greeting />
        <SearchBox initialQuery="react" />
      </div>
    );
  }
}
