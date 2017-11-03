// @flow
import React from 'React';
import ClickerPage from './common/ClickerPage';
import LectureStudent from './lecture/LectureStudent';
import SignInCard from './sign_in/SignInCard';

import io from 'socket.io-client';

type Props = {};

class Playground extends React.Component<Props, void> {
  socket: Object;

  componentDidMount (): void {
    this.socket = io('http://localhost:3000');
  }

  render (): React.Element<any> {
    return (
      <ClickerPage>
        <SignInCard />
        <LectureStudent />
      </ClickerPage>
    );
  }
}

export default Playground;
