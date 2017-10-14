// @flow
import ClickerPage from './common/ClickerPage';
import React from 'react';
import SignInCard from './sign_in/SignInCard';

class SignIn extends React.Component {
  render (): React.Element<any> {
    return (
      <ClickerPage>
        <SignInCard />
      </ClickerPage>
    );
  }
}

export default SignIn;
