import React, { Component } from 'react';

import { FormGroup, ControlLabel, Button, Table } from 'react-bootstrap';

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
    if (this.props.question) {
      const choices = this.props.question.choices.map((choice, i) => (
        <tr key={i}>
          <td>{choice}</td>
          <td>{this.props.responses.filter((r) => r === choice).length}</td>
        </tr>
      ));

      return (
        <div>
          <FormGroup>
            <ControlLabel>Current Question: {this.props.question.text}</ControlLabel>
          </FormGroup>
          <Button bsStyle='danger' onClick={() => this.handleEnd()}>End Question</Button>
          <h3>Responses</h3>
          <Table striped bordered>
            <thead>
              <tr>
                <th>Response</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {choices}
            </tbody>
          </Table>
        </div>
      );
    }

    return <QuestionCreator {...this.props} />
  }
}

export default LectureProfessor;