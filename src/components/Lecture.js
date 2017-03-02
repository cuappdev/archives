import React, { Component } from 'react';
import { Link } from 'react-router';
import io from 'socket.io-client';

class Lecture extends Component {
  constructor(props) {
    super(props);

    this.state = {
      connected: false
    };
  }

  componentDidMount() {
    const socket = io(':3000');

    socket.on('connect', () => {
      console.log(`Connected to socket with id ${socket.id}`);
      this.setState({
        connected: true
      })
    });

    socket.on('disconnect', () => {
      this.setState({
        connected: false
      });
    });

    socket.on('helloworld', (data) => {
      this.setState({
        message: `Server says: ${data}`
      });
    });

    this.setState({
      socket: socket
    });
  }

  componentWillUnmount() {
    this.state.socket.close();
  }

  handleClick() {
    const message = 'Hey server!';
    this.state.socket.emit('helloworld', message);
  }

  render() {
    return (
      <div>
        <Link to='/'>Back to Home</Link>
        <p>{this.state.connected ? 'Connected' : 'Disconnected. Attempting to reconnect...'}</p>
        <button onClick={() => this.handleClick()}>Say hi!</button>
        <p>{this.state.message}</p>
      </div>
    );
  }
}

export default Lecture;