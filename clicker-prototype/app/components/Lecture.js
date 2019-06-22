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
      responses: {},
      messages: {},
      studentCount: 0,
      professorCount: 0
    };
  }

  componentDidMount() {
    const route = process.env.NODE_ENV === 'develop' ? '/' : ':3000';
    const socket = io(route, { query: `userType=${this.props.userType}`});

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
        responses: {},
        studentCount: 0,
        professorCount: 0
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
        return {
          responses: Object.assign({}, prevState.responses, data.responses)
        };
      });
    });

    socket.on('sc', (data) => {
      this.setState({
        studentCount: data
      });
    });

    socket.on('pc', (data) => {
      this.setState({
        professorCount: data
      });
    });

    socket.on('sm', (data) => {
      this.setState((prevState, id) => {
        return {
          messages: Object.assign({}, prevState.messages, data.messages)
        };
      });
    })

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
              <h4>Connected</h4>
              <p>{this.state.studentCount} students</p>
              <p>{this.state.professorCount} professors</p>
            </Alert>
            {
              this.props.userType === 'students'
                ? <LectureStudent {...this.state} handleResponse={(i) => this.handleResponse(i)} />
                : <LectureProfessor {...this.state} />
            }
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
