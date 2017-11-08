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
  Input
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
  questions: Array<Object>,
  onToggleEditLectureModal: (boolean) => void,
  onEditLectureSave: (Object) => void,
  onToggleQuestionModal: (boolean) => void,
  onQuestionSave: (Object) => void
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

  onSelectQuestion = (index: number): void => {
    // TODO: open question modal for specific question
  }

  _buildQuestions (): List {
    return (
      <List></List>
    );
  }

  _sideBar = (): Segment => (
    <Segment raised>
      <Button
        onClick={ () => this.props.onToggleQuestionModal(true) }
        content='Create Question'
        fluid
      />
      {this.props.questionModalOpen &&
        <LectureQuestionCreator
          open={this.props.questionModalOpen}
          lectureTitle={this.props.lectureTitle}
          onClose={ () => this.props.onToggleQuestionModal(false) }
          onSave={this.props.onQuestionSave}
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
    const questions = this._buildQuestions();

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
            {questions}
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
    dispatch(actions.toggleEditLectureModal(show));
  };
  const onEditLectureSave = (data: Object) => {
    dispatch(actions.editLectureSave(data));
  };
  const onToggleQuestionModal = (show: boolean) => {
    dispatch(actions.toggleQuestionModal(show));
  };
  const onQuestionSave = (data: Object) => {
    dispatch(actions.lectureQuestionSave(data));
  };

  return {
    onToggleEditLectureModal,
    onEditLectureSave,
    onToggleQuestionModal,
    onQuestionSave
  };
};

export default connect(stateProps, dispatchProps)(LecturePage);
