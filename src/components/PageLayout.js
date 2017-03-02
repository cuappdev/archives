import React, { Component } from 'react';

import io from 'socket.io-client';
const socket = io(':3000');

class PageLayout extends Component {

  componentWillMount() {
    socket.on('connect', () => {
      console.log(`Connected to socket with id ${socket.id}`);
    });
  }

  render() {
    return (
      <div>
        Clicker app!
        {this.props.children}
      </div>
    );
  }
}

export default PageLayout;