import React, { Component } from 'react';
import { Link } from 'react-router';

import { ListGroup, ListGroupItem } from 'react-bootstrap';

class Home extends Component {
  render() {
    return (
      <div>
        <h3>Welcome to the Cornell AppDev Clicker app!</h3>
        <ListGroup>
          <ListGroupItem><Link to='/lecture'>Student Sign In</Link></ListGroupItem>
          <ListGroupItem><a href='/lecture/professor'>Professor Sign In</a></ListGroupItem>
        </ListGroup>
      </div>
    );
  }
}

export default Home;
