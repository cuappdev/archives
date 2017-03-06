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
      response: null,
      responses: {}
    };
  }

  componentDidMount() {
    const socket = io('/', { query: `userType=${this.props.userType}`});

    this.setState({
      socket: socket
    });

    socket.on('connect', () => {
      console.log('Connected to socket');
      this.setState({
        connected: true
      });
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from socket');
      this.setState({
        connected: false,
        question: null,
        response: null,
        responses: {}
      });
    });

    socket.on('bq', (data) => this.setState(data));

    socket.on('eq', () => {
      this.setState({
        question: null,
        response: null,
        responses: {}
      });
    });

    socket.on('rq', (data) => {
      this.setState((prevState, id) => {
        return { responses: data.responses || Object.assign({}, prevState.responses, data.response) }
      });
    });

  }

  componentWillUnmount() {
    this.state.socket.close();
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
          {this.props.userType === 'students' ? <LectureStudent {...this.state} /> : <LectureProfessor {...this.state} />}
        </Panel>
      </div>
    );
  }
}

export default Lecture;
