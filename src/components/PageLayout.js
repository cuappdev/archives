import React, { Component } from 'react';

class PageLayout extends Component {
  render() {
    return (
      <div>
        Clicker app!
        {this.props.children}
      </div>
    );
  }
}

export default PageLayout;