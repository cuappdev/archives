// @flow
import { Link } from 'react-router';
import React from 'react';

import { COLORS } from './constants';

type Props = {};
type State = {};

class ClickerHeader extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {};
  }

  _renderLinks (): React.Element<any> {
    return (
      <div>
        <Link to='/signin' style={styles.link}>Sign In</Link>
        <Link to='/dashboard' style={styles.link}>Dashboard</Link>
      </div>
    );
  }

  render (): React.Element<any> {
    return (
      <div style={styles.root}>
        <Link to='/' style={styles.title}>CliquePod</Link>
        {this._renderLinks()}
      </div>
    );
  }
}

const styles = {
  root: {
    borderBottom: `2px solid ${COLORS.OFF_WHITE}`,
    display: 'flex',
    flexDirection: 'row',
    padding: '24px 0px',
    width: '100%'
  },
  title: {
    color: COLORS.DARK_GRAY,
    fontSize: '18px',
    marginLeft: '24px',
    marginRight: 'auto',
    textDecoration: 'none'
  },
  link: {
    color: COLORS.DARK_GRAY,
    fontSize: '14px',
    marginRight: '20px',
    textDecoration: 'none'
  }
};

export default ClickerHeader;