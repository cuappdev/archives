//@flow
import React from 'react';
import {
  Modal,
  Tab,
  Button,
  Header
} from 'semantic-ui-react';

import LectureQuestionCreatorItem from './LectureQuestionCreatorItem';

type Props = {
  open: boolean,
  lectureTitle: string,
  onClose: () => void,
  data?: Object
};
type State = {
  activeQuestionIndex: number,
  questionTitle: string
};

class LectureQuestionCreator extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    console.log(props);
    this.state = {
      questionTitle: '',
      activeQuestionIndex: 0
    };
  }

  handleTabChange = (activeIndex: number): void => {
    this.setState({
      activeQuestionIndex: activeIndex
    });
  }

  _buildQuestionPanes (): Tab {
    const questionTypes = ['Multiple Choice', 'Free Response', 'Ordering'];
    const panes = questionTypes.map((questionType) => {
      const paramType = questionType.charAt(0).toLowerCase() + questionType.slice(1).replace(' ', '');
      return {
        menuItem: questionType,
        render: () => (
          <Tab.Pane attached={false}>
            <LectureQuestionCreatorItem
              questionType={paramType}
              questionTitle={this.state.questionTitle}
            />
          </Tab.Pane>
        )
      };
    });
    return panes;
  }

  render (): React.Element<any> {
    const questionPanes = this._buildQuestionPanes();

    return (
      <Modal
        open={this.props.open}
        onClose={this.props.onClose}
        dimmer='blurring'
        closeIcon
      >
        <Modal.Header icon='book' content={this.props.lectureTitle} />
        <Modal.Content>
          <Header floated='left'>Question Type</Header>
          <Tab
            menu={{ secondary: true }}
            panes={questionPanes}
            onTabChange={ (_, data) => this.handleTabChange(data.activeIndex) }
            activeIndex={this.state.activeQuestionIndex}
          />
        </Modal.Content>
        <Modal.Actions>

        </Modal.Actions>
      </Modal>
    );
  }
}

export default LectureQuestionCreator;
