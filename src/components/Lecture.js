import React, { Component } from 'react';
import { Link } from 'react-router';
import io from 'socket.io-client';

import LectureStudent from './LectureStudent';
import LectureProfessor from './LectureProfessor';

class Lecture extends Component {
  constructor(props) {
    super(props);

    this.state = {
      connected: false,
      question: null
    };
  }

  componentDidMount() {
    const socket = io(':3000', {query: `userType=${this.props.userType}`});

    this.setState({
      socket: socket
    });

    socket.on('connect', () => {
      console.log(`Connected to socket with id ${socket.id}`);
      this.setState({
        connected: true
      });
    });

    socket.on('disconnect', () => {
      this.setState({
        connected: false
      });
    });

    socket.on('bq', (data) => {
      this.setState({
        question: data
      });
    });

    socket.on('eq', (data) => {
      this.setState({
        question: null
      });
    });
    
  }

  componentWillUnmount() {
    this.state.socket.close();
  }

  handleSend() {
    const message = 'Hey server!';
    this.state.socket.emit('helloworld', message);
  }

  render() {
    return (
      <div>
        <Link to='/'>Back to Home</Link>
        <h3>Lecture</h3>
        <p>You are a {this.props.userType == 'students' ? 'Student' : 'Professor'}!</p>
        <p style={{ 'color': this.state.connected ? 'green' : 'red' }}>{this.state.connected ? 'Connected' : 'Disconnected. Attempting to reconnect...'}</p>
        {this.props.userType == 'students' ? <LectureStudent {...this.state} /> : <LectureProfessor {...this.state} />}
      </div>
    );
  }
}

export default Lecture;