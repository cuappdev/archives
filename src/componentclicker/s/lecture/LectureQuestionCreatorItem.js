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
  multipleChoiceHandlers: Object,
  freeResponseHandlers: Object,
  mapIndexToLetter: (number) => string
};
type State = {};

class LectureQuestionCreatorItem extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {};
  }

  _multipleChoiceOptions = (): Array<Object> => {
    if (!this.props.data) return [];
    const options = this.props.data.options.map((option, idx) => {
      return (
        <Segment basic key={idx} style={styles.multipleChoiceSegment}>
          <Label basic size='large' style={{ border: 'none' }}>
            {`${option.id}.`}
          </Label>
          <div style={styles.multipleChoiceItem}>
            <Input iconPosition='left' placeholder={`Option ${idx}...`} fluid>
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

  _renderMultipleChoiceQuestion = () => {
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

  _renderFreeResponseQuestion = () => {
    return (
      <div>
        <Header size='small' color='grey'>
          Answer:
        </Header>
        <Form>
          <TextArea
            placeholder='What is the answer?'
            value={this.props.data ? this.props.data.optionalAnswer : ''}
            onChange={ (_,d) => this.props.freeResponseHandlers.onChangeAnswer(d) }
            autoHeight
            rows={2}
          />
        </Form>
      </div>
    );
  };

  render (): React.Element<any> {
    console.log('Data for question item', this.props.data);
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
