//@flow
import React from 'react';
import {
  Input,
  Header,
  Form,
  TextArea,
  Button,
  Segment,
  Label,
  Icon,
  Modal
} from 'semantic-ui-react';
import { QUESTION_TYPES, COLORS } from '../common/constants';

import MultipleChoiceCorrectAnswerModal from './MultipleChoiceCorrectAnswerModal';

type Props = {
  questionType: string,
  data: Object,
  multipleChoiceHandlers: Object,
  freeResponseHandlers: Object,
  mapIndexToLetter: (number) => string
};
type State = {
  setCorrectAnswerModalOpen: boolean
};

class LectureQuestionCreatorItem extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {
      setCorrectAnswerModalOpen: false
    };
  }

  onShowSetCorrectAnswerModal = (show: boolean): void => {
    // TODO: Filter out options with no value
    if (show) {
      this.props.multipleChoiceHandlers.onFilterOptions();
    }
    this.setState({
      setCorrectAnswerModalOpen: show
    });
  }

  onSetCorrectAnswerSave = (letter: string): void => {
    this.props.multipleChoiceHandlers.onSelectAnswer(letter);
    this.onShowSetCorrectAnswerModal(false);
  }

  setCorrectAnswerButtonDisabled = (): boolean => {
    const enabled = this.props.data.options.reduce((acc, option) => {
      console.log(acc, option.description);
      return acc || option.description !== '';
    }, false);
    return !enabled;
  }

  _multipleChoiceOptions = (): Array<Object> => {
    const options = this.props.data.options.map((option, idx) => {
      return (
        <Segment basic key={idx} style={styles.multipleChoiceSegment}>
          <Label basic size='large' style={{ border: 'none' }}>
            {`${option.id}.`}
          </Label>
          <div
            style={{
              ...styles.multipleChoiceItem,
              ...(this.props.data.answer === option.id ? styles.correctItem : {})
            }}
          >
            <Input iconPosition='left' placeholder={`Option ${idx+1}...`} fluid>
              <Icon name='content' />
              <input
                value={option.description}
                onChange={ (e) =>
                  this.props.multipleChoiceHandlers.onUpdateOption(e, idx)
                }
              />
            </Input>
          </div>
          <Button
            icon='trash'
            onClick={ () =>
              this.props.multipleChoiceHandlers.onRemoveOption(idx)
            }
            style={{ marginLeft: '15px' }}
          />
        </Segment>
      );
    });
    return options;
  }

  _multipleChoiceQuestionItem = () => {
    return (
      <div>
        <Header size='small' color='grey'>
          Answers:
        </Header>
        {this._multipleChoiceOptions()}
        <Button
          onClick={this.props.multipleChoiceHandlers.onAddOption}
          content='Add Option'
          icon='plus'
          compact
          basic
          style={{ marginTop: '10px' }}
        />
        <Button
          onClick={ () => this.onShowSetCorrectAnswerModal(true) }
          content='Set Correct Answer'
          icon='checkmark'
          disabled={this.setCorrectAnswerButtonDisabled()}
          compact
          basic
          style={{ marginTop: '10px' }}
        />
        {this.state.setCorrectAnswerModalOpen &&
          <MultipleChoiceCorrectAnswerModal
            data={this.props.data}
            onSave={this.onSetCorrectAnswerSave}
            onClose={ () => this.onShowSetCorrectAnswerModal(false) }
          />
        }
      </div>
    );
  };

  _multipleAnswerQuestionItem = () => {
    return (
      <Header>Multiple Answer</Header>
    );
  };

  _rankingQuestionItem = () => {
    return (
      <Header>Ranking</Header>
    );
  };

  _freeResponseQuestionItem = () => {
    return (
      <div>
        <Header size='small' color='grey'>
          Answer:
        </Header>
        <Form>
          <TextArea
            placeholder='What is the answer?'
            value={this.props.data.optionalAnswer}
            onChange={ (_,d) => this.props.freeResponseHandlers.onChangeAnswer(d) }
            rows={2}
            style={{ resize: 'none' }}
          />
        </Form>
      </div>
    );
  };

  render (): React.Element<any> {
    // console.log('Data for question item', this.props.data);
    switch (this.props.questionType) {
      case QUESTION_TYPES.MULTIPLE_CHOICE:
        return this._multipleChoiceQuestionItem();
      case QUESTION_TYPES.MULTIPLE_ANSWER:
        return this._multipleAnswerQuestionItem();
      case QUESTION_TYPES.RANKING:
        return this._rankingQuestionItem();
      case QUESTION_TYPES.FREE_RESPONSE:
      default:
        return this._freeResponseQuestionItem();
    }
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

export default LectureQuestionCreatorItem;
