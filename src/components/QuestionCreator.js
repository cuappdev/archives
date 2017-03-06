import React, { Component } from 'react';

import { FormGroup, InputGroup, ControlLabel, FormControl, HelpBlock, Checkbox, Button } from 'react-bootstrap';

class QuestionCreator extends Component {
  constructor(props) {
    super(props);

    this.state = {
      questionValue: '',
      newChoiceValue: '',
      choices: []
    };
  }

  getValidationState() {
    const length = this.state.questionValue.length;
    if (length > 0) return 'success'
  }

  handleQuestionChange(e) {
    this.setState({ questionValue: e.target.value });
  }

  handleChoiceChange(e) {
    this.setState({ newChoiceValue: e.target.value });
  }

  handleChoiceKeyPress(e) {
    if (e.key === 'Enter' && this.state.newChoiceValue) {
      this.handleAddChoice();
    }
  }

  handleAddChoice() {
    this.setState((prevState, props) => {
      return {
        choices: prevState.choices.concat([prevState.newChoiceValue]),
        newChoiceValue: ''
      };
    });
  }

  handleSend() {
    let data = {
      'text': this.state.questionValue,
      'choices': this.state.choices
    };

    this.props.socket.emit('bq', { question: data });
  }

  render() {
    const choices = this.state.choices.map((choice, i) => (
      <Checkbox checked key={i}>
        {choice}
      </Checkbox>
    ));

    return (
      <form>
        <FormGroup
          controlId='formBasicText'
          validationState={this.getValidationState()}
        >
          <ControlLabel>Question</ControlLabel>
          <FormControl
            type='text'
            value={this.state.questionValue}
            placeholder='Enter a Question'
            onChange={(e) => this.handleQuestionChange(e)}
          />
          <FormControl.Feedback />
        </FormGroup>
        <FormGroup>
          <label>Choices</label>
          {choices}
          <InputGroup>
            <FormControl
              type='text'
              value={this.state.newChoiceValue}
              placeholder='Add response choice...'
              onChange={(e) => this.handleChoiceChange(e)}
              onKeyPress={(e) => this.handleChoiceKeyPress(e)}
            />
            <InputGroup.Button>
              <Button bsStyle='primary' disabled={!this.state.newChoiceValue} onClick={() => this.handleAddChoice()}>Add</Button>
            </InputGroup.Button>
          </InputGroup>
        </FormGroup>
        <Button bsStyle='primary' disabled={this.getValidationState() != 'success'} onClick={() => this.handleSend()}>
          Send Question
        </Button>
      </form>
    );
  }
}

export default QuestionCreator;
