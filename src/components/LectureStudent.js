import React, { Component } from 'react';

class LectureStudent extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    if (this.props.question) {
      const choices = this.props.question.choices;

      if (choices) {
        const choiceComponent = choices.length === 0
          ? <input type='text' />
          : <form>{
              choices.map((choice, i) => (
                <li key={choice.id}>
                  {choice}
                </li>
              ))
            }</form>;
      }

      return (
        <div>
          <h3>Question:</h3>
          <p>{this.props.question.text}</p>
          {choiceComponent}
        </div>
      );
    } else {
      return (
        <div>
          <p>Waiting for next question...</p>
        </div>
      );
    }
  }
}

export default LectureStudent;