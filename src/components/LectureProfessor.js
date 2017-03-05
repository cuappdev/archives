import React, { Component } from 'react';

import { FormGroup, ControlLabel, Button, Table } from 'react-bootstrap';

import QuestionCreator from './QuestionCreator';
import LectureVisualizer from './LectureVisualizer';

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

      // Get response counts
      const responseCounts = {}
      for (var address in this.props.responses) {
        if (!this.props.responses.hasOwnProperty(address)) continue;

        const response = this.props.responses[address];
        if (response in responseCounts) responseCounts[response] += 1;
        else responseCounts[response] = 1
      }

      // Get responses

      // Create response table
      const responseList = this.props.question.choices.map((choice, i) => (
        <tr key={i}>
          <td>{choice}</td>
          <td>{responseCounts[choice] || 0}</td>
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
              {responseList}
            </tbody>
          </Table>
          <LectureVisualizer responseCounts={responseCounts} choices={this.props.question.choices} />
        </div>
      );
    }

    return <QuestionCreator {...this.props} />
  }
}

export default LectureProfessor;
