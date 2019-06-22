// @flow
import Cookies from 'universal-cookie';
import Playground from './Playground';
import React from 'react';

import { connect } from 'react-redux';
import actions from './actions';
import { COLORS } from './common/constants';

const cookies = new Cookies();

type Props = {
  sessionToken: ?string,
  setSessionToken: string => void,
  children: any
};

class App extends React.Component<void, Props, void> {
  props: Props;

  componentDidMount (): void {
    const token = cookies.get('accessToken');
    if (token) this.props.setSessionToken(token);
  }

  render (): React.Element<any> {
    console.log('Session token: ' + (this.props.sessionToken || 'null'));
    // TODO - to test, replace this function with `Playground`
    return (
      <div style={styles.app}>
        {this.props.children}
      </div>
    );
  }
}

// Overarching app styles - will be the defaults of every Component
// in the application
const styles = {
  app: {
    fontFamily: COLORS.FONT_FAMILY,
    width: '100%'
  }
};

const select = (store: Object) => {
  return {
    sessionToken: store.auth.sessionToken
  };
};

const acts = (dispatch: Function) => {
  const setSessionToken = (token: string) => {
    dispatch(actions.AuthActions.setSessionToken(token));
  };

  return {
    setSessionToken
  };
};

export default connect(select, acts)(App);