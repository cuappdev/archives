import React, { Component } from 'react';
import { Link } from 'react-router';

class NotFound extends Component {
  render() {
    return (
      <div>
        <h2>Oops, that page doesn't exist.</h2>
        <Link to='/'>Home</Link>
      </div>
    );
  }
}

export default NotFound;