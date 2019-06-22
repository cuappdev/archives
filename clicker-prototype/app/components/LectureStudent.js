import React, { Component } from 'react';
import { Panel, ListGroup, ListGroupItem, FormGroup, FormControl, Button } from 'react-bootstrap';

import utils from '../utils';

class LectureStudent extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  handleSend(e, i) {
    this.props.handleResponse(i);
    this.props.socket.emit('rq', { response: this.props.question.choices[i] });
  }

  handlePingChange(e) {
    this.setState({
      pingText: e.target.value
    });
  }

  handlePingSend() {
    this.props.socket.emit('sm', { message: this.state.pingText })
    this.setState({
      pingText: ''
    });
  }

  render() {
    var question = (
      <div>Waiting for next question...</div>
    );

    if (this.props.question) {
      const choices = this.props.question.choices;

      const choiceList = !choices || choices.length === 0
        ? (<input type='text' />)
        : choices.map((choice, i) => (
            <ListGroupItem key={i} onClick={(e) => this.handleSend(e, i)} active={this.props.response === choice}>
              <span><strong>{utils.alphabet[i]}</strong> {choice}</span>
            </ListGroupItem>
          ));

      question = (
        <div>
          <h3>{this.props.question.text}</h3>
          <ListGroup>
            {choiceList}
          </ListGroup>
        </div>
      );
    }

    return (
      <div>
        <Panel header={'Student'}>
          {question}
        </Panel>
        <Panel header={'Message the professors:'}>
          <FormGroup controlId='formControlsTextarea'>
            <FormControl
              componentClass='textarea'
              onChange={(e) => this.handlePingChange(e)}
              placeholder='Do you need help? Did we make a typo?'
              value={this.state.pingText}
            />
          </FormGroup>
          <Button bsStyle='primary' onClick={() => this.handlePingSend()}>Send</Button>
        </Panel>
      </div>
    );
  }
}

export default LectureStudent;
