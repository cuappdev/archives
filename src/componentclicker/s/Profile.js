// @flow
import Cookies from 'universal-cookie';
import ClickerPage from './common/ClickerPage';
import React from 'react';

import axios from 'axios';
import constants from './common/constants';

type Props = {};
type State = {
  user: ?Object
};

const cookies = new Cookies();

class Profile extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);
    this.state = {
      user: null
    };
  }

  componentDidMount (): void {
    const accessToken = cookies.get('accessToken');
    if (accessToken) {
      console.log(accessToken);
      axios.post(`/api/v1/users/me?accessToken=${accessToken}`)
        .then((response: Object) => {
          console.log(response);
          this.setState({
            user: response.data.data
          });
        });
    }
  }

  _renderUser (user: Object): React.Element<any> {
    return (
      <div>
        {user.fields.firstName}<br />
        {user.fields.lastName}<br />
        {user.fields.email}<br />
      </div>
    );
  }

  render (): React.Element<any> {
    return (
      <ClickerPage>
        <div style={styles.root}>
          {this.state.user ? this._renderUser(this.state.user) : null}
        </div>
      </ClickerPage>
    );
  }
}

const styles = {
  root: {
    color: constants.DARK_GRAY,
    margin: '100px auto',
    width: '150px'
  }
};

export default Profile;
