import React, { Component } from 'react';

import { FormGroup, ControlLabel, Button, ListGroup, ListGroupItem } from 'react-bootstrap';

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

    const responses = this.props.responses.map((response, i) => (
      <ListGroupItem key={i}>
        {response}
      </ListGroupItem>
    ));

    return this.props.question
      ? (
          <div>
            <FormGroup>
              <ControlLabel>Current Question: {this.props.question.text}</ControlLabel>
            </FormGroup>
            <Button bsStyle='danger' onClick={() => this.handleEnd()}>End Question</Button>
            <h3>Responses</h3>
            <ListGroup>
              {responses}
            </ListGroup>
          </div>
        )
      : (
          <QuestionCreator {...this.props} />
        );
  }
}

export default LectureProfessor;