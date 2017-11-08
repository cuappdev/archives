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
  Icon
} from 'semantic-ui-react';
import { QUESTION_TYPES, COLORS } from '../common/constants';

type Props = {
  questionType: string,
  data?: Object,
  ref: (Object) => void
};
type State = {
  freeResponseAnswer: string,
  multipleChoiceOptions: Array<Object>,
  rankingOptions: Array<Object>,
};

class LectureQuestionCreatorItem extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {
      freeResponseAnswer: '',
      multipleChoiceOptions: [],
      rankingOptions: [],
      ...(props.data || {})
    };
  }

  _mapIndexToLetter = (index: number): string => {
    const letterA = 65;
    return String.fromCharCode(letterA + index);
  }

  onAddMultipleChoiceOption = (): void => {
    const options = this.state.multipleChoiceOptions;
    options.push({
      value: '',
      isAnswer: false
    });
    this.setState({
      multipleChoiceOptions: options
    });
  }

  onRemoveMultipleChoiceOption = (index: number): void => {
    const options = this.state.multipleChoiceOptions;
    options.splice(index, 1);
    this.setState({
      multipleChoiceOptions: options
    });
  }

  onUpdateMultipleChoiceOptionValue = (event: Object, index: number): void => {
    const options = this.state.multipleChoiceOptions;
    options[index].value = event.target.value;
    this.setState({
      multipleChoiceOptions: options
    });
  }

  onToggleMultipleChoiceOptionAnswer = (index: number): void => {
    const options = this.state.multipleChoiceOptions;
    options[index].isAnswer = !options[index].isAnswer;
    this.setState({
      multipleChoiceOptions: options
    });
  }

  onSortMultipleChoiceOptions = (sortedOptions: Array<Object>, dropEvent: Object): void => {
    console.log('On sort', sortedOptions, dropEvent);
  }

  _buildMultipleChoiceOptions = (): Array<Object> => {
    const options = this.state.multipleChoiceOptions.map((option, idx) => {
      var letter = this._mapIndexToLetter(idx);
      return (
        <Segment basic key={idx} style={styles.multipleChoiceSegment}>
          <Label basic size='large' style={{ border: 'none' }}>
            {`${letter}.`}
          </Label>
          <div style={styles.multipleChoiceItem}>
            <Input iconPosition='left' placeholder={`Option ${idx}...`} fluid>
              <Icon name='content' />
              <input
                value={option.value}
                onChange={ (e) => this.onUpdateMultipleChoiceOptionValue(e, idx) }
              />
            </Input>
          </div>
          <Button
            icon='trash'
            onClick={ () => this.onRemoveMultipleChoiceOption(idx) }
            style={{ marginLeft: '15px' }}
          />
        </Segment>
      );
    });
    return options;
  }

  _renderMultipleChoiceQuestion = () => {
    const options = this._buildMultipleChoiceOptions();

    return (
      <div>
        <Header size='small' color='grey'>
          Answers:
        </Header>
        {options}
        <Button
          onClick={this.onAddMultipleChoiceOption}
          content='Add Option'
          icon='plus'
          compact
          basic
          style={{ marginTop: '10px' }}
        />
      </div>
    );
  };

  _renderMultipleAnswerQuestion = () => {
    return (
      <Header>Multiple Answer</Header>
    );
  };

  _renderRankingQuestion = () => {
    return (
      <Header>Ranking</Header>
    );
  };

  onFreeResponseAnswerChange = (event: Object): void => {
    this.setState({
      freeResponseAnswer: event.target.value
    });
  }

  _renderFreeResponseQuestion = () => {
    return (
      <div>
        <Header size='small' color='grey'>
          Answer:
        </Header>
        <Form>
          <TextArea
            placeholder='What is the answer?'
            value={this.state.freeResponseAnswer}
            onChange={this.onFreeResponseAnswerChange}
            autoHeight
            rows={2}
          />
        </Form>
      </div>
    );
  };

  _renderQuestionItem = () => {
    switch (this.props.questionType) {
      case QUESTION_TYPES.MULTIPLE_CHOICE:
        return this._renderMultipleChoiceQuestion();
      case QUESTION_TYPES.MULTIPLE_ANSWER:
        return this._renderMultipleAnswerQuestion();
      case QUESTION_TYPES.RANKING:
        return this._renderRankingQuestion();
      case QUESTION_TYPES.FREE_RESPONSE:
      default:
        return this._renderFreeResponseQuestion();
    }
  }

  render (): React.Element<any> {
    return (
      <div>
        {this._renderQuestionItem()}
      </div>
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
  multipleChoiceItemCorrect: {
    padding: '10px',
    width: '80%',
    display: 'inline-block',
    borderRadius: '4px',
    backgroundColor: COLORS.GREEN
  }
}

export default LectureQuestionCreatorItem;
