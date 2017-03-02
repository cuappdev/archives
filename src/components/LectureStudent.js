import React, { Component } from 'react';

class LectureStudent extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    return this.props.question
      ? (
          <div>
            <h3>Question:</h3>
            <p>{this.props.question.text}</p>
          </div>
        )
      : (
          <div>
            <p>Waiting for next question...</p>
          </div>
        );
  }
}

export default LectureStudent;