//@flow
import React from 'react';
import {
  Input
} from 'semantic-ui-react';

type Props = {
  questionType: string,
  questionTitle: string
};
type State = {

};

class LectureQuestionCreatorItem extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {

    };
  }

  render (): React.Element<any> {
    return (
      <p>{this.props.questionType}</p>
    );
  }
}

export default LectureQuestionCreatorItem;
