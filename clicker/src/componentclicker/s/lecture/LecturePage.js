//@flow
import React from 'react';
import { connect } from 'react-redux';
import {
  Breadcrumb,
  Header,
  Divider,
  Grid,
  Segment,
  Button,
  List,
  Modal,
  Input,
  Card
} from 'semantic-ui-react';
import actions from '../actions';
import type { QuestionType } from '../common/constants';

import ClickerPage from '../common/ClickerPage';
import EditLectureModal from './EditLectureModal';
import LectureQuestionCreator from './LectureQuestionCreator';

type Props = {
  location: Object,
  courseTitle: string,
  lectureTitle: string,
  lectureDate?: string,
  editLectureModalOpen: boolean,
  questionModalOpen: boolean,
  questionModalData?: Object,
  questions: Array<Object>,
  editLectureHandlers: Object,
  editQuestionHandlers: Object
};
type State = {
  courseTitle: string,
  lectureId?: number
};

class LecturePage extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      ...props.location.state
    };
  }

  _breadcrumbs (): Breadcrumb {
    return (
      <Breadcrumb size='tiny'>
        <Breadcrumb.Section href='/'>
          Home
        </Breadcrumb.Section>
        <Breadcrumb.Divider icon='right chevron' />
        <Breadcrumb.Section href='/dashboard'>
          {this.state.courseTitle}
        </Breadcrumb.Section>
        <Breadcrumb.Divider icon='right chevron' />
        <Breadcrumb.Section active>
          {this.state.lectureId ? 'Lecture' : 'New Lecture'}
        </Breadcrumb.Section>
      </Breadcrumb>
    );
  }

  abbreviateQuestionType = (questionType: QuestionType): string => {
    return questionType.split('_').map((el) => el.charAt(0)).join('');
  };

  handleOpenEditLectureModal = (): void => {
    this.props.editLectureHandlers.onToggleEditLectureModal(true);
  }

  handleCloseEditLectureModal = (): void => {
    this.props.editLectureHandlers.onToggleEditLectureModal(false);
  }

  handleCreateQuestionClick = (): void => {
    this.props.editQuestionHandlers.onEditQuestion();
  }

  _questionCards (): Card.Group {
    const questionCards = this.props.questions.map((question) => {
      return (
        <Card key={question.id} fluid>
          <Card.Content>
            <Button
              onClick={ () =>
                this.props.editQuestionHandlers.onDeleteQuestion(question.id)
              }
              icon='trash'
              circular
              floated='right'
            />
            <Button
              onClick={ () =>
                this.props.editQuestionHandlers.onEditQuestion(question)
              }
              icon='edit'
              circular
              floated='right'
            />
            <Card.Header>
              {this.abbreviateQuestionType(question.type)}
            </Card.Header>
            <Card.Description>
              {question.text}
            </Card.Description>
          </Card.Content>
        </Card>
      );
    });

    return (
      <Card.Group>
        {questionCards}
      </Card.Group>
    );
  }

  _sideBar = (): Segment => (
    <Segment raised>
      <Button
        onClick={this.handleCreateQuestionClick}
        content='Create Question'
        fluid
      />
      {this.props.questionModalOpen &&
        <LectureQuestionCreator
          open={this.props.questionModalOpen}
          lectureTitle={this.props.lectureTitle}
          questionData={this.props.questionModalData}
          onCancel={this.props.editQuestionHandlers.onCancelEditQuestion}
          onSave={this.props.editQuestionHandlers.onSaveQuestion}
        />
      }
      <br></br>
      <Button.Group basic compact vertical icon labeled>
        <Button
          onClick={this.handleOpenEditLectureModal}
          compact
          content='Edit'
          icon='edit'
        />
        <EditLectureModal
          isOpen={this.props.editLectureModalOpen}
          onClose={this.handleCloseEditLectureModal}
          onSave={this.props.editLectureHandlers.onEditLectureSave}
          lectureTitle={this.props.lectureTitle}
        />
        <Button compact content='Save' icon='save' />
        <Button compact content='Delete' icon='archive' />
      </Button.Group>
    </Segment>
  );

  render (): React.Element<any> {
    return (
      <ClickerPage>
        {this._breadcrumbs()}
        <Header color='grey' size='medium'>
          {this.state.courseTitle}
        </Header>
        <Header size='medium' floated='left'>
          {this.props.lectureTitle}
        </Header>
        <Header size='medium' floated='right'>
          {this.props.lectureDate}
        </Header>
        <Divider clearing />
        <Grid centered columns={2}>
          <Grid.Column width={12}>
            {this._questionCards()}
          </Grid.Column>
          <Grid.Column width={4}>
            {this._sideBar()}
          </Grid.Column>
        </Grid>
      </ClickerPage>
    );
  }
}

// Map store to props
const stateProps = (store: Object) => {
  return {
    ...store.lecture
  };
};

// Map dispatch actions to props
const dispatchProps = (dispatch: Function) => {
  const onToggleEditLectureModal = (show: boolean) => {
    dispatch(actions.LectureActions.toggleEditModal(show));
  };
  const onEditLectureSave = (data: Object) => {
    dispatch(actions.LectureActions.saveLecture(data));
  };
  const onEditQuestion = (data?: Object) => {
    dispatch(actions.LectureActions.editQuestion(data));
  };
  const onCancelEditQuestion = () => {
    dispatch(actions.LectureActions.cancelEditQuestion());
  };
  const onSaveQuestion = (data: Object) => {
    dispatch(actions.LectureActions.saveQuestion(data));
  };
  const onDeleteQuestion = (id: number) => {
    dispatch(actions.LectureActions.deleteQuestion(id));
  }
  
  const editLectureHandlers = {
    onToggleEditLectureModal,
    onEditLectureSave
  };
  const editQuestionHandlers = {
    onEditQuestion,
    onCancelEditQuestion,
    onSaveQuestion,
    onDeleteQuestion
  };

  return {
    editLectureHandlers,
    editQuestionHandlers
  };
};

export default connect(stateProps, dispatchProps)(LecturePage);