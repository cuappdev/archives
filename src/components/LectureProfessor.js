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
      const responseCounts = {}
      for (var address in this.props.responses) {
        if (!this.props.responses.hasOwnProperty(address)) continue;

        const response = this.props.responses[address];
        if (response in responseCounts) responseCounts[response] += 1;
        else responseCounts[response] = 1
      }

      const responses = Object.keys(responseCounts).map((response, i) => (
        <tr key={i}>
          <td>{response}</td>
          <td>{responseCounts[response]}</td>
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
              {responses}
            </tbody>
          </Table>
        </div>
      );
    }

    return <QuestionCreator {...this.props} />
  }
}

export default LectureProfessor;
