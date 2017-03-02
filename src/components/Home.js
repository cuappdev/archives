import React, { Component } from 'react';
import { Link } from 'react-router';

class Home extends Component { 
  render() {
    return (
      <div>
        <Link to='/lecture'>Go to lecture</Link>
        <p>Welcome to the CUAppDev Clicker app!</p>
      </div>
    );
  }
}

export default Home;