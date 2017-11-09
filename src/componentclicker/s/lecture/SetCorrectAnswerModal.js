// @flow
import React from 'react';
import {
  Modal,
  Button,
  Segment,
  Label,
  Icon,
  Input
} from 'semantic-ui-react';
import { COLORS } from '../common/constants';

type Props = {
  data: Object,
  onSave: (string) => void,
  onClose: () => void
};
type State = {
  correctAnswer: string
};

class SetCorrectAnswerModal extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      correctAnswer: props.data.answer
    };
  }

  setCorrectAnswer = (letter: string): void => {
    this.setState(prevState => {
      return {
        correctAnswer: prevState.correctAnswer === letter ? '' : letter
      };
    });
  }

  _multipleChoiceOptions = (): Array<Object> => {
    const options = this.props.data.options.map((option, idx) => {
      return (
        <Segment
          key={idx}
          onClick={ () => this.setCorrectAnswer(option.id) }
          basic
          style={styles.multipleChoiceSegment}
        >
          <Label basic size='large' style={{ border: 'none' }}>
            {`${option.id}.`}
          </Label>
          <div
            style={{
              ...styles.multipleChoiceItem,
              ...(this.state.correctAnswer === option.id ? styles.correctItem : {})
            }}
          >
            <Input iconPosition='left' fluid>
              <Icon name='content' />
              <input
                value={option.description}
                readOnly
              />
            </Input>
          </div>
        </Segment>
      );
    });
    return options;
  }

  render (): React.Element<any> {
    return (
      <Modal
        open={true}
        dimmer='inverted'
        size='small'
        onClose={this.props.onClose}
      >
        <Modal.Header>
          Set the correct answer:
        </Modal.Header>
        <Modal.Content>
          {this._multipleChoiceOptions()}
        </Modal.Content>
        <Modal.Actions>
          <Button
            content='Set As Correct'
            icon='checkmark'
            labelPosition='right'
            onClick={ () => this.props.onSave(this.state.correctAnswer) }
          />
        </Modal.Actions>
      </Modal>
    );
  }
}

const styles = {
  multipleChoiceSegment: {
    margin: '0px',
    padding: '5px'
  },
  multipleChoiceItem: {
    padding: '10px',
    width: '80%',
    display: 'inline-block',
    borderRadius: '4px',
    backgroundColor: COLORS.WHITE
  },
  correctItem: {
    backgroundColor: COLORS.GREEN
  }
}

export default SetCorrectAnswerModal;
