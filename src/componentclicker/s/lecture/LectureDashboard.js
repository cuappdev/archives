//@flow
import React from 'react';
import { browserHistory } from 'react-router';
import {
  Header,
  Icon,
  Tab,
  Grid,
  Segment,
  Button,
  Breadcrumb
} from 'semantic-ui-react';

import ClickerPage from '../common/ClickerPage';

type Props = {
  courseId: number
};
type State = {
  courseTitle: string,
  lectures: Array<Object>
};

class LectureDashboard extends React.Component<Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    console.log(props);
    // TODO: Fetch course information given the courseId
    // Placeholder values...
    const courseTitle = 'CS 4700: Introduction to Artificial Intelligence';
    const lectures = [
      {
        id: 0,
        title: 'The History of Artificial Intelligence',
        date: '10/08/2017',
        questions: [1,2,3]
      }
    ];

    this.state = {
      courseTitle: courseTitle,
      lectures: lectures
    };
  }

  onCreateLecture = (): void => {
    console.log('Create lecture clicked');
    browserHistory.push('/createLecture');
  }

  onSelectLecture = (id: number): void => {
    console.log(`Clicked lecture with id: ${id}`);
  }

  _buildLecturePane = (): Grid => {
    const lectures = this.state.lectures.map((lecture: Object) => {
      return (
        <Segment onClick={ () => this.onSelectLecture(lecture.id) }>
          <Header size='small'>{`${lecture.date}: ${lecture.title}`}</Header>
          <Header size='tiny' color='grey'>{`${lecture.questions.length} Questions`}</Header>
        </Segment>
      );
    });
    const rhs = (
      <Segment raised textAlign='center' height='200px'>
        <Button
          onClick={this.onCreateLecture}
          centered
          inverse>
          Create Lecture
        </Button>
      </Segment>
    );

    return (
      <Grid centered columns={2}>
        <Grid.Column width={12}>
          {lectures}
        </Grid.Column>
        <Grid.Column width={4}>
          {rhs}
        </Grid.Column>
      </Grid>
    );
  }

  render(): React.Element<any> {
    const lecturePane = this._buildLecturePane();
    const panes = [
      {
        menuItem: 'Lectures',
        render: () => (
          <Tab.Pane attached={false}>
            {lecturePane}
          </Tab.Pane>
        )
      },
      {
        menuItem: 'Analytics',
        render: () => (
          <Tab.Pane attached={false}>
            <Header>TODO</Header>
          </Tab.Pane>
        )
      }
    ];
    return (
      <div>
        <Breadcrumb size='tiny'>
          <Breadcrumb.Section link>Dashboard</Breadcrumb.Section>
          <Breadcrumb.Divider icon='right chevron'/>
          <Breadcrumb.Section active>Course</Breadcrumb.Section>
        </Breadcrumb>
        <Header color='grey' size='medium'>
          {this.state.courseTitle}
        </Header>
        <Tab menu={{ secondary: true, pointing: true }} panes={panes} />
      </div>
    );
  }
}

const styles = {
}

export default LectureDashboard;
