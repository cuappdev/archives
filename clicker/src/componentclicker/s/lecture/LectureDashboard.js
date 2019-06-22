//@flow
import React from 'react';
import { browserHistory, Link } from 'react-router';
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

class LectureDashboard extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    console.log(props);
    // TODO: This component needs to be hooked up with redux
    // and fully implement, these should be props
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
    browserHistory.push({
      pathname: '/lecture/create',
      state: {
        courseTitle: this.state.courseTitle
      }
    });
  }

  onSelectLecture = (id: number): void => {
    // TODO: Push to lecture page for specified lectureId
  }

  _breadCrumbs = (): Breadcrumb => (
    <Breadcrumb size='tiny'>
      <Breadcrumb.Section href='/' >
        Home
      </Breadcrumb.Section>
      <Breadcrumb.Divider icon='right chevron'/>
      <Breadcrumb.Section active>
        {this.state.courseTitle}
      </Breadcrumb.Section>
    </Breadcrumb>
  );

  _lecturePane = (): Grid => {
    const lectures = this.state.lectures.map((lecture: Object) => {
      return (
        <Segment key={lecture.id} onClick={ () => this.onSelectLecture(lecture.id) }>
          <Header size='small'>{`${lecture.date}: ${lecture.title}`}</Header>
          <Header size='tiny' color='grey'>{`${lecture.questions.length} Questions`}</Header>
        </Segment>
      );
    });
    const sideBar = (
      <Segment raised textAlign='center' height='200px'>
        <Button fluid onClick={this.onCreateLecture}>
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
          {sideBar}
        </Grid.Column>
      </Grid>
    );
  }

  _tabPanes = (): Array<Object> => {
    return [
      {
        menuItem: 'Lectures',
        render: () => (
          <Tab.Pane attached={false}>
            {this._lecturePane()}
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
  }

  render(): React.Element<any> {
    return (
      <div>
        {this._breadCrumbs()}
        <Header color='grey' size='medium'>
          {this.state.courseTitle}
        </Header>
        <Tab
          menu={{ secondary: true, pointing: true }}
          panes={this._tabPanes()}
        />
      </div>
    );
  }
}

export default LectureDashboard;
