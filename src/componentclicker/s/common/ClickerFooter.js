// @flow
import React from 'react';

import { COLORS } from './constants';

type Props = {
};

class ClickerFooter extends React.Component<void, Props, void> {
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
    borderTop: `1px solid ${COLORS.OFF_WHITE}`,
    display: 'flex',
    flexDirection: 'row',
    margin: '0px auto',
    padding: '24px 0px',
    width: '90%'
  },
  text: {
    color: COLORS.DARK_GRAY
  }
};

export default ClickerFooter;
