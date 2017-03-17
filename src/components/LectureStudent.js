import React, { Component } from 'react';
import { ListGroup, ListGroupItem } from 'react-bootstrap';

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

  render() {
    if (this.props.question) {
      const choices = this.props.question.choices;

      const choiceList = !choices || choices.length === 0
        ? (<input type='text' />)
        : choices.map((choice, i) => (
            <ListGroupItem key={i} onClick={(e) => this.handleSend(e, i)} active={this.props.response === choice}>
              <span><strong>{utils.alphabet[i]}</strong> {choice}</span>
            </ListGroupItem>
          ));

      return (
        <div>
          <h3>{this.props.question.text}</h3>
          <ListGroup>
            {choiceList}
          </ListGroup>
        </div>
      );
    }

    return (
      <div>Waiting for next question...</div>
    );
  }
}

export default LectureStudent;
