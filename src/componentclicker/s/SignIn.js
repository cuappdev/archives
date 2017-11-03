// @flow
import ClickerPage from './common/ClickerPage';
import React from 'React';
import SignInCard from './sign_in/SignInCard';

class SignIn extends React.Component<void, void> {
  render (): React.Element<any> {
    return (
      <ClickerPage>
        <SignInCard />
      </ClickerPage>
    );
  }
}

export default SignIn;
