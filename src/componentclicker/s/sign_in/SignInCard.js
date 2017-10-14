// @flow
import ClickerCard from '../common/Clickercard';
import ClickerGoogleSignInButton from '../common/ClickerGoogleSignInButton';
import React from 'react';

import constants from '../common/constants';

class SignInCard extends React.Component {
  componentDidMount (): void {
  }

  render (): React.Element<any> {
    return (
      <ClickerCard
        style={styles.card}
        title='Sign In'>
        <div style={styles.contents}>
          <div style={styles.description}>
            Sign into CliquePod through Google!  Be sure to use your
            Cornell Google account to sign in.
          </div>
          <ClickerGoogleSignInButton height={36} />
        </div>
      </ClickerCard>
    );
  }
}

const styles = {
  card: {
    margin: '50px auto',
    maxWidth: '600px'
  },
  description: {
    color: constants.DARK_GRAY,
    fontSize: '12px',
    marginBottom: '12px',
    textAlign: 'center'
  },
  contents: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: '24px'
  }
};

export default SignInCard;
