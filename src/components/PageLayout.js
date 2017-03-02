import React, { Component } from 'react';

class PageLayout extends Component {

  render() {
    return (
      <div style={{ minWidth: 300, width: '80%', margin: 'auto' }}>
        <h1>Clicker</h1>
        {this.props.children}
      </div>
    );
  }
}

export default PageLayout;