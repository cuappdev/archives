//@flow
import React from 'react';
import {
  Modal,
  Tab,
  Button,
  Header,
  Form,
  TextArea
} from 'semantic-ui-react';
import type { QuestionType } from '../common/constants';
import { QUESTION_TYPES } from '../common/constants';

import LectureQuestionCreatorItem from './LectureQuestionCreatorItem';

type Props = {
  open: boolean,
  lectureTitle: string,
  onClose: () => void,
  onSave: (data: Object) => void,
  data?: Object
};
type State = {
  questionTitle: string,
  questionType: QuestionType,
  activeQuestionTypeIndex: number
};

class LectureQuestionCreator extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    console.log(props);
    var state = {
      questionTitle: '',
      questionType: QUESTION_TYPES.MULTIPLE_CHOICE,
      ...(props.data || {})
    };
    state.activeQuestionTypeIndex = this._mapQuestionTypeToTabIndex(state.questionType);
    this.state = state;
    console.log('Question creator state:', this.state);
  }

  _makeQuestionTypeReadable (questionType: QuestionType): string {
    const elements = questionType.split('_');
    const updatedElements = elements.map((el) => {
      return el.charAt(0) + el.slice(1).toLowerCase();
    });
    return updatedElements.join(' ');
  }

  _mapTabIndexToQuestionType (index: number): QuestionType {
    Object.values(QUESTION_TYPES).forEach((qt, idx) => {
      if (idx === index) return qt;
    });
    return QUESTION_TYPES.MULTIPLE_CHOICE;
  }

  _mapQuestionTypeToTabIndex (questionType: QuestionType): number {
    Object.values(QUESTION_TYPES).forEach((qt, idx) => {
      if (qt === questionType) return idx;
    });
    return 0;
  }

  handleTabChange = (activeIndex: number): void => {
    const questionType = this._mapTabIndexToQuestionType(activeIndex);
    this.setState({
      questionType: questionType,
      activeQuestionTypeIndex: activeIndex
    });
  }

  onQuestionTitleChange = (event: Object): void => {
    this.setState({
      questionTitle: event.target.value
    });
  }

  _buildQuestionPanes = (): Tab => {
    const panes = Object.keys(QUESTION_TYPES).map((questionType) => {
      return {
        menuItem: this._makeQuestionTypeReadable(questionType),
        render: () => (
          <Tab.Pane attached={false}>
            <LectureQuestionCreatorItem
              questionTitle={this.state.questionTitle}
              questionType={questionType}
              data={this.props.data}
            />
          </Tab.Pane>
        )
      };
    });
    return panes;
  }

  onSave = (): void => {
    this.props.onSave({
      questionTitle: this.state.questionTitle,
      questionType: this.state.questionType
    });
  }

  render (): React.Element<any> {
    console.log('Rendering question creator...');
    const questionPanes = this._buildQuestionPanes();

    return (
      <Modal
        open={this.props.open}
        onClose={this.props.onClose}
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
              autoHeight
              rows={2}
            />
          </Form>
          <Header size='small' color='grey'>
            Question Type:
          </Header>
          <Tab
            menu={{ color: 'blue', secondary: true, attached: false, tabular: false }}
            panes={questionPanes}
            onTabChange={ (_, data) => this.handleTabChange(data.activeIndex) }
            activeIndex={this.state.activeQuestionTypeIndex}
          />
        </Modal.Content>
        <Modal.Actions>
          <Button
            onClick={this.props.onClose}
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
