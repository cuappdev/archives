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
  questionData?: Object,
  onCancel: () => void,
  onSave: (data: Object) => void
};
type State = {
  questionId?: number,
  questionText: string,
  questionType: QuestionType,
  activeQuestionTypeIndex: number,
  questionData: Object
};

class LectureQuestionCreator extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    var state = {};
    if (props.questionData) {
      state = {
        questionId: props.questionData.id,
        questionText: props.questionData.text,
        questionType: props.questionData.type,
        activeQuestionTypeIndex: this._mapQuestionTypeToMenuIndex(props.questionData.type)
      }
    } else {
      state = {
        questionId: null,
        questionText: '',
        questionType: QUESTION_TYPES.MULTIPLE_CHOICE,
        activeQuestionTypeIndex: 0
      }
    }
    this.state = {
      ...state,
      questionData: this._initializeQuestionData(props.questionData)
    };
    console.log('Question creator state:', this.state);
  }

  _initializeQuestionData (data?: Object): Object {
    const questionData = {
      [QUESTION_TYPES.MULTIPLE_CHOICE]: { options: [], answer: '' },
      [QUESTION_TYPES.FREE_RESPONSE]: { optionalAnswer: '' },
      [QUESTION_TYPES.MULTIPLE_ANSWER]: { options: [], answer: [] },
      [QUESTION_TYPES.RANKING]: { options: [], answer: [] }
    };
    if (data) {
      var updatedData = Object.assign({}, data);
      delete updatedData.id;
      delete updatedData.text;
      delete updatedData.type;
      questionData[data.type] = { ...updatedData };
    }
    console.log('Question data', questionData);
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

  _mapIndexToLetter = (index: number): string => {
    const letterA = 65;
    return String.fromCharCode(letterA + index);
  }

  _mapLetterToIndex = (letter: string): number => {
    return letter.charCodeAt(0) - 65;
  }

  onQuestionTextChange = (event: Object): void => {
    this.setState({
      questionText: event.target.value
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
    if (!this.state.questionText) {
      console.log('Missing question title');
      return false;
    }
    return true;
  }

  onSave = (): void => {
    if (!this._validateQuestion()) {
      // TODO: Show error/missing fields message
      return;
    }
    this.props.onSave({
      questionId: this.state.questionId,
      questionText: this.state.questionText,
      questionType: this.state.questionType,
      data: this.state.questionData[this.state.questionType]
    });
  }

  /*
   * Functional props for LectureQuestionCreatorItem
   */
  setMultipleChoiceState = (data: Object): void => {
    this.setState(prevState => {
      return {
        questionData: {
          ...prevState.questionData,
          [QUESTION_TYPES.MULTIPLE_CHOICE]: data
        }
      };
    });
  }

  onAddMultipleChoiceOption = (): void => {
    const data = this.state.questionData[QUESTION_TYPES.MULTIPLE_CHOICE];
    data.options.push({
      id: this._mapIndexToLetter(data.options.length),
      description: ''
    });
    this.setMultipleChoiceState(data);
  }

  onRemoveMultipleChoiceOption = (index: number): void => {
    var data = this.state.questionData[QUESTION_TYPES.MULTIPLE_CHOICE];
    // Update answer id
    if (data.answer === data.options[index].id) {
      data.answer = '';
    } else if (data.answer > data.options[index].id) {
      const answerIndex = this._mapLetterToIndex(data.answer);
      data.answer = this._mapIndexToLetter(answerIndex-1);
    }
    // Update question options
    data.options.splice(index, 1);
    data.options = data.options.map((option, idx) => ({
      ...option,
      id: this._mapIndexToLetter(idx)
    }));
    this.setMultipleChoiceState(data);
  }

  onUpdateMultipleChoiceOption = (event: Object, index: number): void => {
    const data = this.state.questionData[QUESTION_TYPES.MULTIPLE_CHOICE];
    data.options[index].description = event.target.value;
    this.setMultipleChoiceState(data);
  }

  onSelectMultipleChoiceAnswer = (letter: string): void => {
    const data = this.state.questionData[QUESTION_TYPES.MULTIPLE_CHOICE];
    data.answer = letter;
    this.setMultipleChoiceState(data);
  }

  onChangeFreeResponseAnswer = (input: Object): void => {
    const data = this.state.questionData[QUESTION_TYPES.FREE_RESPONSE];
    this.setState(prevState => {
      return {
        questionData: {
          ...prevState.questionData,
          [QUESTION_TYPES.FREE_RESPONSE]: {
            ...data,
            optionalAnswer: input.value
          }
        }
      };
    });
  }

  /*
   * End functional props for LectureQuestionCreatorItem
   */

  _lectureQuestionCreatorItem = () => {
    const multipleChoiceHandlers = {
      onAddOption: this.onAddMultipleChoiceOption,
      onRemoveOption: this.onRemoveMultipleChoiceOption,
      onUpdateOption: this.onUpdateMultipleChoiceOption,
      onSelectAnswer: this.onSelectMultipleChoiceAnswer
    };
    const freeResponseHandlers = {
      onChangeAnswer: this.onChangeFreeResponseAnswer
    };
    return (
      <LectureQuestionCreatorItem
        questionType={this.state.questionType}
        data={this.state.questionData[this.state.questionType]}
        multipleChoiceHandlers={multipleChoiceHandlers}
        freeResponseHandlers={freeResponseHandlers}
        mapIndexToLetter={this._mapIndexToLetter}
      />
    );
  };

  render (): React.Element<any> {
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
              value={this.state.questionText}
              onChange={this.onQuestionTextChange}
              rows={2}
              style={{ resize: 'none' }}
            />
          </Form>
          <Header size='small' color='grey'>
            Question Type:
          </Header>
          {this._questionTypeMenu()}
          {this._lectureQuestionCreatorItem()}
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
            primary
          />
        </Modal.Actions>
      </Modal>
    );
  }
}

export default LectureQuestionCreator;
