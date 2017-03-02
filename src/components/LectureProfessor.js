import React, { Component } from 'react';

import { Button } from 'react-bootstrap';

import QuestionCreator from './QuestionCreator';

class LectureProfessor extends Component {
  constructor(props) {
    super(props);

  }

  handleTextChange(e) {
    this.setState({
      text: e.target.value
    });
  }

  handleEnd() {
    this.props.socket.emit('eq');
  }

  render() {
    return this.props.question
      ? (
          <button onClick={() => this.handleEnd()}>End Question</button>
        )
      : (
          <QuestionCreator {...this.props} />
        );
  }
}

export default LectureProfessor;