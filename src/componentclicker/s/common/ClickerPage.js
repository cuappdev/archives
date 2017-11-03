// @flow
import ClickerFooter from './ClickerFooter';
import ClickerHeader from './ClickerHeader';
import React from 'react';

type Props = {
  children?: any
}

class ClickerPage extends React.Component<Props, void> {
  props: Props;

  render (): React.Element<any> {
    return (
      <div>
        <ClickerHeader />
        <div style={styles.content}>{this.props.children}</div>
        <ClickerFooter />
      </div>
    );
  }
}

const styles = {
  content: {
    minHeight: '70vh',
    padding: '20px'
  }
};

export default ClickerPage;
