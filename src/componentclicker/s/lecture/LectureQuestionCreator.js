//@flow
import React from 'react';
import {
  Modal,
  Menu,
  Button,
  Header,
  Form,
  TextArea
} from 'semantic-ui-react';
import type { QuestionType } from '../common/constants';
import { QUESTION_TYPES } from '../common/constants';
import actions from '../actions';

import LectureQuestionCreatorItem from './LectureQuestionCreatorItem';

type Props = {
  open: boolean,
  lectureTitle: string,
  questionId?: number,
  questionTitle?: string,
  questionType?: QuestionType,
  questionData?: Object,
  onCancel: () => void,
  onSave: (data: Object) => void
};
type State = {
  questionTitle: string,
  questionType: QuestionType,
  activeQuestionTypeIndex: number,
  questionData: Object
};

class LectureQuestionCreator extends React.Component<void, Props, State> {
  props: Props;
  state: State;
  questionItemRef: Object;

  constructor (props: Props) {
    super(props);
    var state = {
      questionTitle: props.questionTitle || '',
      questionType: props.questionType || QUESTION_TYPES.MULTIPLE_CHOICE,
      activeQuestionTypeIndex: 0,
      questionData: this._initializeQuestionData(props.questionType, props.questionData)
    };
    state.activeQuestionTypeIndex = this._mapQuestionTypeToMenuIndex(state.questionType);
    this.state = state;
    console.log('Question creator state:', this.state);
  }

  _initializeQuestionData (questionType?: QuestionType, data?: Object): Object {
    const questionData = {};
    Object.keys(QUESTION_TYPES).forEach((questionType) => {
      questionData[questionType] = {};
    });
    if (questionType && data) {
      questionData[questionType] = { ...data };
    }
    return questionData;
  }

  _makeQuestionTypeReadable (questionType: QuestionType): string {
    const elements = questionType.split('_');
    const updatedElements = elements.map((el) => {
      return el.charAt(0) + el.slice(1).toLowerCase();
    });
    return updatedElements.join(' ');
  }

  _mapQuestionTypeToMenuIndex (questionType: QuestionType): number {
    Object.values(QUESTION_TYPES).forEach((qt, idx) => {
      if (qt === questionType) return idx;
    });
    return 0;
  }

  onQuestionTitleChange = (event: Object): void => {
    this.setState({
      questionTitle: event.target.value
    });
  }

  onQuestionTypeChange = (questionType: QuestionType, index: number): void => {
    if (index !== this.state.activeQuestionTypeIndex) {
      this.setState({
        questionType: questionType,
        activeQuestionTypeIndex: index
      });
    }
  }

  _questionTypeMenu = (): Menu => {
    const menuItems = Object.keys(QUESTION_TYPES).map((questionType, idx) => {
      const itemName = this._makeQuestionTypeReadable(questionType);
      return (
        <Menu.Item
          key={idx}
          name={itemName}
          active={this.state.activeQuestionTypeIndex === idx}
          onClick={ () => this.onQuestionTypeChange(questionType, idx) }
        />
      );
    });
    return (
      <Menu defaultActiveIndex={0} secondary color='blue'>
        {menuItems}
      </Menu>
    );
  }

  _validateQuestion = (): boolean => {
    // TODO: Validate question on save
    if (!this.state.questionTitle) {
      console.log('Missing question title');
      return false;
    }
    return true;
  }

  onSave = (): void => {
    console.log('Question Item Ref', this.questionItemRef);
    if (!this._validateQuestion()) {
      // TODO: Show error/missing fields message
      return;
    }
    const data = function(self) {
      switch (self.state.questionType) {
        case QUESTION_TYPES.MULTIPLE_CHOICE:
        case QUESTION_TYPES.MULTIPLE_ANSWER:
          return self.questionItemRef.state.multipleChoiceOptions;
        case QUESTION_TYPES.FREE_RESPONSE:
          return self.questionItemRef.state.freeResponseAnswer;
        case QUESTION_TYPES.RANKING:
          return self.questionItemRef.state.rankingOptions;
        default: return null;
      }
    }(this);
    this.props.onSave({
      questionId: this.props.questionId,
      questionTitle: this.state.questionTitle,
      questionType: this.state.questionType,
      data: data
    });
  }

  render (): React.Element<any> {
    console.log('Rendering question creator...');
    return (
      <Modal
        open={this.props.open}
        onClose={this.props.onCancel}
        size='large'
        dimmer='blurring'
      >
        <Modal.Header icon='book' content={this.props.lectureTitle} />
        <Modal.Content>
          <Header size='small' color='grey'>
            Question:
          </Header>
          <Form>
            <TextArea
              placeholder='What is the question?'
              value={this.state.questionTitle}
              onChange={this.onQuestionTitleChange}
              rows={2}
              style={{ resize: 'none' }}
            />
          </Form>
          <Header size='small' color='grey'>
            Question Type:
          </Header>
          {this._questionTypeMenu()}
          <LectureQuestionCreatorItem
            questionType={this.state.questionType}
            data={this.state.questionData[this.state.questionType]}
            ref={ (item) => { this.questionItemRef = item; } }
          />
        </Modal.Content>
        <Modal.Actions>
          <Button
            onClick={this.props.onCancel}
            content='Cancel'
          />
          <Button
            onClick={this.onSave}
            content='Save'
            icon='save'
            labelPosition='right'
            positive
          />
        </Modal.Actions>
      </Modal>
    );
  }
}

export default LectureQuestionCreator;
