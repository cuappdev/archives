import React, { Component } from 'react';

class PageLayout extends Component {

  render() {
    return (
      <div>
        <h1>Clicker</h1>
        {this.props.children}
      </div>
    );
  }
}

export default PageLayout;