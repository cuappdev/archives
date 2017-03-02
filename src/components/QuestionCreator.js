import React, { Component } from 'react';

import { FormGroup, ControlLabel, FormControl, HelpBlock } from 'react-bootstrap';

class QuestionCreator extends Component {
  constructor(props) {
    super(props);

    this.state = {
      value: ''
    };
  }

  getValidationState() {
    const length = this.state.value.length;
    if (this.state.value.length > 0) return 'success'
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  handleSend() {
    this.props.socket.emit('bq', { 'text': this.state.text });
  }

  render() {
    return (
      <form>
        <FormGroup
          controlId='formBasicText'
          validationState={this.getValidationState()}
        >
          <ControlLabel>Create a Question</ControlLabel>
          <FormControl
            type='text'
            value={this.state.value}
            placeholder='Enter a Question'
            onChange={(e) => this.handleChange(e)}
          />
          <FormControl.Feedback />
          <HelpBlock>Validation is based on string length.</HelpBlock>
        </FormGroup>
      </form>
    );
  }
}

export default QuestionCreator;