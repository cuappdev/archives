// @flow
import React from 'react';
import ClickerButton from './ClickerButton';

type Props = {
  data: Object,
  onClick: number => void,
  selection: number
};
type State = {
  question: string,
  choices: Object
}

// TODO - Make this nice with designs
class ClickerQuestion extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);

    this.state = {
      question: props.data.question,
      choices: props.data.choices
    };
  }

  render (): React.Element<any> {
    const choices = this.state.choices.map((el, i) => (
      <ClickerButton
        key={i}
        onClick={ () => this.props.onClick(i) }
        inverse={(i === this.props.selection)} >
        {el}
      </ClickerButton>
    ));
    return (
      <div>
        <h3>{this.state.question}</h3>
        {choices}
      </div>
    );
  }
}

export default ClickerQuestion;
