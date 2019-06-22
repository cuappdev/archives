// @flow
import React from 'react';
import { COLORS } from './constants';

type Props = {
  placeholder?: string,
  value: string,
  onChange: Object => void,
  width?: string
};
type State = {
  placeholder: string
};

// TODO - Make this conform to designs
class ClickerTextInput extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      placeholder: this.props.placeholder ? this.props.placeholder : ''
    };
  }

  render (): React.Element<any> {
    var style = (this.props.width) ? { ...style, width: this.props.width } : styles.textInput;
    return (
      <input
        style={style}
        type='text'
        placeholder={this.state.placeholder}
        value={this.props.value}
        onChange={this.props.onChange}
      />
    );
  }
}

const styles = {
  textInput: {
    height: '20px',
    width: 'calc(100% - 42px)',
    margin: '10px',
    padding: '5px 10px',
    backgroundColor: COLORS.WHITE,
    color: COLORS.DARK_GRAY,
    border: `1px solid ${COLORS.GRAY}`,
    fontSize: '12px',
    fontFamily: COLORS.FONT_FAMILY,
    display: 'block'
  }
}

export default ClickerTextInput
