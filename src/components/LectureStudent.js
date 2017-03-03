import React, { Component } from 'react';

import { Radio } from 'react-bootstrap';

class LectureStudent extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  handleSend(e, i) {
    this.setState({
      choiceIndex: i
    });

    this.props.socket.emit('rq', this.props.question.choices[i]);
  }

  render() {
    if (this.props.question) {
      const choices = this.props.question.choices;

      const choiceComponent = !choices || choices.length === 0
        ? <input type='text' />
        : <form>{
            choices.map((choice, i) => (
              <Radio key={i} onClick={(e) => this.handleSend(e, i)} checked={this.state.choiceIndex === i}>
                {choice}
              </Radio>
            ))
          }</form>;

      return (
        <div>
          <h3>{this.props.question.text}</h3>
          {choiceComponent}
        </div>
      );
    }
    
    return (
      <div>Waiting for next question...</div>
    );
  }
}

export default LectureStudent;