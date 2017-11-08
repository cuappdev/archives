// @flow
import React from 'react';
import { COLORS } from './constants';

type ButtonSize = 'small' | 'medium' | 'large';

type Props = {
  onClick: () => void,
  disabled?: boolean,
  size?: ButtonSize,
  inverse?: boolean,
  children: any
};
type State = {
  size: string,
  inverse: boolean
};

// TODO - Make this component nice with designs
class ClickerButton extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      size: (props.size ? props.size : 'medium'),
      inverse: (props.inverse ? props.inverse : false)
    };
  }

  render (): React.Element<any> {
    var style = styles.button;
    style = { ...style, ...(this.state.inverse ? styles.inverse : styles.normal) };
    style = { ...style, ...styles[this.state.size] };

    return (
      <button
        style={style}
        onClick={this.props.onClick}
        disabled={this.props.disabled ? this.props.disabled : false}
      >
        {this.props.children}
      </button>
    )
  }
}

const styles = {
  button: {
    margin: '10px',
    padding: '10px 15px',
    outline: 'none',
    cursor: 'pointer'
  },
  normal: {
    backgroundColor: COLORS.WHITE,
    color: COLORS.DARK_GRAY,
    border: `2px solid ${COLORS.LIGHT_GRAY}`,
    fontFamily: COLORS.FONT_FAMILY
  },
  inverse: {
    backgroundColor: COLORS.LIGHT_GRAY,
    color: COLORS.WHITE,
    border: `2px solid ${COLORS.LIGHT_GRAY}`,
    fontFamily: COLORS.FONT_FAMILY
  },
  small: {
    fontSize: '11px',
  },
  medium: {
    fontSize: '14px'
  },
  large: {
    fontSize: '18px'
  }
}

export default ClickerButton;
