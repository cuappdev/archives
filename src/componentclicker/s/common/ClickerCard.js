// @flow
import React from 'react';

import constants from './constants';

type Props = {
  children?: any,
  style?: Object,
  title?: string,
};

class ClickerCard extends React.Component<void, Props, void> {
  props: Props;

  render (): React.Element<any> {
    return (
      <div style={{
        ...styles.root,
        ...(this.props.style || {})
      }}>
        {this.props.title
          ? <div style={styles.title}>{this.props.title}</div>
          : null}
        <div>
          {/* Contents can be of whatever style the user likes */}
          {this.props.children}
        </div>
      </div>
    );
  }
}

const styles = {
  root: {
    border: `1px solid ${constants.GRAY}`,
    borderRadius: '4px',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'
  },
  title: {
    backgroundColor: constants.OFF_WHITE,
    borderBottom: `1px solid ${constants.GRAY}`,
    color: constants.GRAY,
    fontSize: '12px',
    padding: '4px 12px'
  }
};

export default ClickerCard;
