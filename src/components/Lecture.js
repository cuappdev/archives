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
        return { responses: Object.assign({}, prevState.responses, data.responses) }
      });
    });

  }

  componentWillUnmount() {
    this.state.socket.close();
  }

  handleResponse(i) {
    this.setState({
      response: this.state.question.choices[i]
    });
  }

  render() {
    const lecture = this.state.connected
      ? (
          <div>
            <Alert bsStyle='success'>
              <strong>Connected</strong>
            </Alert>
            <Panel header={this.props.userType == 'students' ? 'Student' : 'Professor'}>
              {
                this.props.userType === 'students'
                  ? <LectureStudent {...this.state} handleResponse={(i) => this.handleResponse(i)} />
                  : <LectureProfessor {...this.state} />
              }
            </Panel>
          </div>
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
        {lecture}
      </div>
    );
  }
}

export default Lecture;
