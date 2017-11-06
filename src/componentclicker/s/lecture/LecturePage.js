//@flow
import React from 'react';
import { Link } from 'react-router';
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

import ClickerPage from '../common/ClickerPage';

type Props = {
  location: Object
};
type State = {
  courseTitle: string,
  lectureTitle: string,
  lectureDate: number,
  questions: Array<Object>,
  editLectureModalOpen: boolean,
  editLectureTitle: string
};

class LecturePage extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      ...props.location.state,
      editLectureModalOpen: false,
      editLectureTitle: ''
    };
    console.log(this.state);
  }

  _buildBreadcrumbs (): Breadcrumb {
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
          New Lecture
        </Breadcrumb.Section>
      </Breadcrumb>
    );
  }

  onCreateQuestion = (): void => {
    console.log('Creating question...');
  }

  handleEditLectureModal = (show: boolean): void => {
    this.setState(prevState => ({
      editLectureModalOpen: show,
      editLectureTitle: prevState.lectureTitle
    }));
  }

  onEditLectureSave = (): void => {
    console.log('Saving edits');
    this.setState(prevState => ({
      editLectureModalOpen: false,
      lectureTitle: prevState.editLectureTitle
    }));
  }

  onEditLectureTitleChange = (value: string): void => {
    this.setState({
      editLectureTitle: value
    });
  }

  _buildQuestions (): List {
    return (
      <List></List>
    );
  }

  _buildSideBar (): Segment {
    return (
      <Segment raised>
        <Modal
          trigger={
            <Button fluid onClick={this.onCreateQuestion}>
              Create Question
            </Button>
          }
          dimmer='inverted'
        >
        </Modal>
        <br></br>
        <Button.Group basic compact vertical icon labeled>
          <Modal
            trigger={
              <Button
                onClick={ () => this.handleEditLectureModal(true) }
                compact
                content='Edit'
                icon='edit'
              />
            }
            open={this.state.editLectureModalOpen}
            onClose={ () => this.handleEditLectureModal(false) }
            dimmer='inverted'
            closeIcon
          >
            <Modal.Header>Edit Lecture</Modal.Header>
            <Modal.Content>
              <Input
                label='Lecture Name'
                placeholder='KMeans Clustering'
                value={this.state.editLectureTitle}
                onChange={ (e) => this.onEditLectureTitleChange(e.target.value) }
              />
            </Modal.Content>
            <Modal.Actions>
              <Button onClick={ () => this.handleEditLectureModal(false) }>
                Cancel
              </Button>
              <Button
                positive
                icon='save'
                labelPosition='right'
                content='Save'
                onClick={ () => this.onEditLectureSave() }
              />
            </Modal.Actions>
          </Modal>
          <Button compact content='Save' icon='save' />
          <Button compact content='Delete' icon='archive' />
        </Button.Group>
      </Segment>
    );
  }

  render(): React.Element<any> {
    const sideBar = this._buildSideBar();
    const questions = this._buildQuestions();

    return (
      <ClickerPage>
        {this._buildBreadcrumbs()}
        <Header color='grey' size='medium'>
          {this.state.courseTitle}
        </Header>
        <Header size='medium' floated='left'>
          {this.state.lectureTitle}
        </Header>
        <Header size='medium' floated='right'>
          {this.state.lectureDate}
        </Header>
        <Divider clearing />
        <Grid centered columns={2}>
          <Grid.Column width={12}>
            {questions}
          </Grid.Column>
          <Grid.Column width={4}>
            {sideBar}
          </Grid.Column>
        </Grid>
      </ClickerPage>
    );
  }
}

export default LecturePage;
