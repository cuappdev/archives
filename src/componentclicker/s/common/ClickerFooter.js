// @flow
import React from 'React';

import constants from './constants';

type Props = {
};

class ClickerFooter extends React.Component<Props, void> {
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
