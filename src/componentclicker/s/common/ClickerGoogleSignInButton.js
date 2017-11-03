// @flow
import Cookies from 'universal-cookie';
import GoogleLogin from 'react-google-login';
import React from 'React';

import { browserHistory } from 'react-router';
import axios from 'axios';
import signInBtn from '../../public/signInBtn.png';

type Props = {
  height?: number,
  style?: Object
};

const cookies = new Cookies();

// TODO - this is a test clientId, replace w/production one
const CLIENT_ID =
  '27973282433-mjc2roekjmcq517o0vaiuqsoctf0e30o.apps.googleusercontent.com';

class SignInCard extends React.Component<Props, void> {
  props: Props;

  _onFailure = (result: Object) => {
    // TODO - handle this gracefully
    console.log(result);
  }

  _onSuccess = (result: Object) => {
    axios.post(`/api/v1/users/google/sign_in?code=${result.code}`)
      .then((response: Object) => {
        const accessToken = response.data.data.access_token;
        cookies.set('accessToken', accessToken, { path: '/' });
        browserHistory.push('/'); // redirect to home
      });
  }

  render (): React.Element<any> {
    return (
      <GoogleLogin
        clientId={CLIENT_ID}
        offline={true}
        responseType='code'
        style={{
          ...styles.btn,
          ...(this.props.style || {})
        }}
        onFailure={this._onFailure}
        onSuccess={this._onSuccess}>
        <img src={signInBtn} style={{
          ...styles.img,
          ...(this.props.height ? { height: `${this.props.height}px` } : {})
        }} />
      </GoogleLogin>
    );
  }
}

const styles = {
  btn: {
    backgroundColor: 'transparent',
    borderWidth: '0px',
    outline: '0px',
    padding: '0px',
    height: 'auto',
    width: 'auto'
  },
  img: {
    height: '48px',
    width: 'auto'
  }
};

export default SignInCard;
