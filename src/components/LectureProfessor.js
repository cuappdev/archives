import React, { Component } from 'react';

import { FormGroup, ControlLabel, Button, ButtonToolbar, Table, Modal, ListGroup, ListGroupItem } from 'react-bootstrap';

import QuestionCreator from './QuestionCreator';
import LectureVisualizer from './LectureVisualizer';

class LectureProfessor extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showVisualizer: false
    }
  }

  handleTextChange(e) {
    this.setState({
      text: e.target.value
    });
  }

  handleEnd() {
    this.props.socket.emit('eq');
  }

  handleVisualizerToggle() {
    this.setState({
      showVisualizer: !this.state.showVisualizer
    })
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

      const choices = this.props.question.choices;

      const choiceList = !choices || choices.length === 0
        ? (<p>Free Response</p>)
        : (
            <ListGroup>
            {
              choices.map((choice, i) => (
                <ListGroupItem key={i}>
                  {choice}
                </ListGroupItem>
              ))
            }
          </ListGroup>
        );

      // Get responses

      // Create response table
      const responseList = this.props.question.choices.map((choice, i) => (
        <tr key={i}>
          <td>{choice}</td>
          <td>{responseCounts[choice] || 0}</td>
        </tr>
      ));

      const numResponses = Object.keys(this.props.responses).length;

      return (
        <div>
          <h3>Current Question</h3>
          <p><strong>{this.props.question.text}</strong></p>
          {choiceList}
          <p>{numResponses} {numResponses == 1 ? 'response' : 'responses'}</p>
          <br />
          <ButtonToolbar>
            <Button bsStyle='danger' onClick={() => this.handleEnd()}>End Question</Button>
            <Button onClick={() => this.handleVisualizerToggle()}>Show Responses</Button>
          </ButtonToolbar>
          <Modal show={this.state.showVisualizer} onHide={() => this.handleVisualizerToggle()}>
            <Modal.Header>Responses</Modal.Header>
            <Modal.Body>
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
              <LectureVisualizer
                responseCounts={responseCounts}
                choices={this.props.question.choices}
                responses={this.props.responses}
              />
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={() => this.handleVisualizerToggle()}>Close</Button>
            </Modal.Footer>
          </Modal>
        </div>
      );
    }

    return <QuestionCreator {...this.props} />
  }
}

export default LectureProfessor;
