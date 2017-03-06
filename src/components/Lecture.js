import React, { Component } from 'react';
import { Link } from 'react-router';
import io from 'socket.io-client';

import { Alert, Panel } from 'react-bootstrap';

import LectureStudent from './LectureStudent';
import LectureProfessor from './LectureProfessor';

class Lecture extends Component {
  constructor(props) {
    super(props);

    this.state = {
      connected: false,
      question: null,
      responses: {}
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
        question: null,
        responses: null,
      });
    });

    socket.on('rq', (data) => {
      this.setState((prevState, id) => {
        return { responses: Object.assign({}, prevState.responses, data) }
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
    const alert = this.state.connected
      ? (
          <Alert bsStyle='success'>
            <strong>Connected</strong>
          </Alert>
        )
      : (
          <Alert bsStyle='warning'>
            <strong>Connecting...</strong>
          </Alert>
        );

    return (
      <div>
        <Link to='/'>Back</Link>
        <h3>Lecture</h3>
        {alert}
        <Panel header={this.props.userType == 'students' ? 'Student' : 'Professor'}>
          {this.props.userType == 'students' ? <LectureStudent {...this.state} /> : <LectureProfessor {...this.state} />}
        </Panel>
      </div>
    );
  }
}

export default Lecture;
