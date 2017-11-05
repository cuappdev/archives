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
  Modal
} from 'semantic-ui-react';

import ClickerPage from '../common/ClickerPage';

type Props = {
  location: Object
};
type State = {
  courseTitle: string,
  questions: Array<Object>
};

class LecturePage extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      ...props.location.state,
      questions: []
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

  _buildQuestions (): List {
    return (
      <List></List>
    );
  }

  _buildSideBar (): Segment {
    return (
      <Segment raised>
        <Button fluid onClick={this.onCreateQuestion}>
          Create Question
        </Button>
        <br></br>
        <Button.Group basic compact vertical icon labeled>
          <Button compact content='Edit' icon='edit' />
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
        <Header size='medium'>
          Lecture Name Here
        </Header>
        <Divider />
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
