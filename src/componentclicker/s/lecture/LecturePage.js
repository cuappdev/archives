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
  onToggleEditLectureModal: (boolean) => void,
  onEditLectureSave: (Object) => void,
  onEditQuestion: (?Object) => void,
  onCancelEditQuestion: () => void,
  onSaveQuestion: (Object) => void
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

  _questionCards (): Card.Group {
    const questionCards = this.props.questions.map((question) => {
      return (
        <Card key={question.id}>
          <Card.Content>
            <Button
              onClick={ () => this.props.onEditQuestion(question) }
              icon='edit'
              circular
              floated='right'
            />
            <Card.Header>{question.type}</Card.Header>
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
        onClick={ () => this.props.onEditQuestion(null) }
        content='Create Question'
        fluid
      />
      {this.props.questionModalOpen &&
        <LectureQuestionCreator
          open={this.props.questionModalOpen}
          lectureTitle={this.props.lectureTitle}
          questionData={this.props.questionModalData}
          onCancel={this.props.onCancelEditQuestion}
          onSave={this.props.onSaveQuestion}
        />
      }
      <br></br>
      <Button.Group basic compact vertical icon labeled>
        <Button
          onClick={ () => this.props.onToggleEditLectureModal(true) }
          compact
          content='Edit'
          icon='edit'
        />
        <EditLectureModal
          open={this.props.editLectureModalOpen}
          onClose={ () => this.props.onToggleEditLectureModal(false) }
          onSave={this.props.onEditLectureSave}
          lectureTitle={this.props.lectureTitle}
        />
        <Button compact content='Save' icon='save' />
        <Button compact content='Delete' icon='archive' />
      </Button.Group>
    </Segment>
  );

  render(): React.Element<any> {
    console.log('Rendering lecture page...');
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
  console.log('Lecture page store', store);
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

  return {
    onToggleEditLectureModal,
    onEditLectureSave,
    onEditQuestion,
    onCancelEditQuestion,
    onSaveQuestion
  };
};

export default connect(stateProps, dispatchProps)(LecturePage);
