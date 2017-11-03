// @flow
import ClickerPage from './common/ClickerPage';
import React from 'react';

type Props = {};
type State = {};

class Page404 extends React.Component<Props, State> {
  props: Props;
  state: State;

  constructor(props: Props) {
    super(props);
    this.state = {
      user: null
    };
  }

  render(): React.Element<*>{
    return (
      <ClickerPage>
        <h1>
          404
        </h1>
      </ClickerPage>
    );
  }
}

export default Page404;
