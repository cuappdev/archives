// @flow
import React from 'react';

import constants from './constants';

class ClickerFooter extends React.Component {
  render (): React.Element<any> {
    return (
      <div style={styles.root}>
        <div style={styles.text}>&copy; Cornell AppDev</div>
      </div>
    );
  }
}

const styles = {
  root: {
    borderTop: `1px solid ${constants.OFF_WHITE}`,
    display: 'flex',
    flexDirection: 'row',
    margin: '0px auto',
    padding: '24px 0px',
    width: '90%'
  },
  text: {
    color: constants.DARK_GRAY
  }
};

export default ClickerFooter;
