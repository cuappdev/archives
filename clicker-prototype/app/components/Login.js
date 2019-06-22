import React, { Component } from 'react';
import { Link } from 'react-router';
import { ControlLabel, FormGroup, FormControl, Button } from 'react-bootstrap';

import validate from '../utils';

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      password: ''
    }
  }

  handlePasswordChange(e) {
    this.setState({
      password: e.target.value
    });
  }

  handleLogin(e) {
    fetch('/login', {
      method: 'POST',
      body: {
        password: this.state.password
      }
    })
    .then(res => validate(res))
    .then(json => {
      console.log(json.success);
    });
  }

  render() {
    return (
      <form>
        <h3>Professor Login</h3>
        <ControlLabel>Working example with validation</ControlLabel>
        <FormGroup>
          <FormControl
            type='password'
            value={this.state.password}
            placeholder='Password'
            onChange={(e) => this.handlePasswordChange(e)}
          />
        </FormGroup>
        <Button onClick={(e) => this.handleLogin(e)}>Login</Button>
      </form>
    );
  }
}

export default Login;
