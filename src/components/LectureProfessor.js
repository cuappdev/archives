import React, { Component } from 'react';

class LectureProfessor extends Component {
  constructor(props) {
    super(props);

  }

  handleTextChange(e) {
    this.setState({
      text: e.target.value
    });
  }

  handleSend() {
    this.props.socket.emit('bq', { 'text': this.state.text });
  }

  handleEnd() {
    this.props.socket.emit('eq');
  }

  render() {
    return this.props.question
      ? (
          <button onClick={() => this.handleEnd()}>End Question</button>
        )
      : (
        <div>
          <input type='text' placeholder='Enter a question...' onChange={(e) => this.handleTextChange(e)} />
          <button onClick={() => this.handleSend()}>Send Question</button>
        </div>
        );
  }
}

export default LectureProfessor;