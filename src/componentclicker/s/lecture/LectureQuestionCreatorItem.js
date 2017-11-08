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
import DragSortableList from 'react-drag-sortable';
import { QUESTION_TYPES } from '../common/constants';

type Props = {
  questionType: string,
  data?: Object
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
    options.slice(index, 1);
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
      return {
        content: (
          <Segment basic>
            <Label basic size='large' style={{ border: 'none' }}>
              <Icon name='content' />{letter}
            </Label>
            <Input
              placeholder={`Option ${idx}...`}
              value={option.value}
              onChange={ (e) => this.onUpdateMultipleChoiceOptionValue(e, idx) }
            />
            <Button
              icon='trash'
            />
          </Segment>
        )
      };
    });
    return options;
  }

  _renderMultipleChoiceQuestion = () => {
    console.log('MC Question rendering');
    const options = this._buildMultipleChoiceOptions();

    return (
      <div>
        <Header size='small' color='grey'>
          Answers:
        </Header>
        <DragSortableList
          items={options}
          // placeholder={placeholder}
          onSort={this.onSortMultipleChoiceOptions}
          moveTransitionDuration={0.3}
          dropBackTransitionDuration={0.3}
          type="vertical"
        />
        <Button
          onClick={this.onAddMultipleChoiceOption}
          content='Add Option'
          icon='plus'
          compact
          basic
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
          Answer (optional):
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

export default LectureQuestionCreatorItem;
