// @flow
import React from 'react';
import {
  Modal,
  Input,
  Button
} from 'semantic-ui-react';

type Props = {
  open: boolean,
  onClose: () => void,
  onSave: (Object) => void,
  lectureTitle: string
};
type State = {
  lectureTitle: string
};

class EditLectureModal extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {
      lectureTitle: props.lectureTitle
    };
  }

  onLectureTitleChange = (event: Object): void => {
    this.setState({
      lectureTitle: event.target.value
    });
  }

  onSave = (): void => {
    this.props.onSave({
      lectureTitle: this.state.lectureTitle
    });
  }

  render (): React.Element<any> {
    return (
      <Modal
        open={this.props.open}
        onClose={this.props.onClose}
        size='small'
        dimmer='blurring'
      >
        <Modal.Header>Lecture Settings</Modal.Header>
        <Modal.Content>
          <Input
            label='Lecture Name'
            placeholder='Type the lecture name here'
            value={this.state.lectureTitle}
            onChange={this.onLectureTitleChange}
            fluid
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

export default EditLectureModal;
