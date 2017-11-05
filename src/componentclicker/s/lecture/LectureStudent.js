// @flow
import React from 'react';
import axios from 'axios';
import io, {Socket} from 'socket.io-client';

import ClickerPage from '../common/ClickerPage';
import ClickerTextInput from '../common/ClickerTextInput';
import ClickerButton from '../common/ClickerButton';
import ClickerQuestion from '../common/ClickerQuestion';

type Props = {};
type State = {
  socket?: Socket,
  connected: boolean,
  lectureId: string,
  currentLecture: string,
  question: Object, // TODO - Create question type
  selection: number
};

class LectureStudent extends React.Component<void, Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);

    this.state = {
      socket: null,
      connected: false,
      lectureId: '',
      currentLecture: '',
      question: {},
      selection: -1
    };
  }

  // Open socket and setup events on component mount
  componentDidMount (): void {
    const socket = io('/', {
      query: {
        userType: 'student',
        netId: 'NET_ID_HERE'
      }
    });

    this.setState({
      socket: socket
    });

    socket.on('connect', () => {
      console.log('Student connected to socket');
      this.setState({
        connected: true
      });
    });

    socket.on('disconnect', () => {
      console.log('Student disconnected from socket');
      this.setState({
        connected: false,
        lectureId: '',
        currentLecture: '',
        question: {},
        selection: -1
      });
    });

    socket.on('question-start', (data: Object) => {
      console.log('Question:');
      console.log(data);
      this.setState({
        question: data,
        selection: -1
      });
    });

    socket.on('question-end', () => {
      console.log(`Submitting response:
        ${this.state.question.choices[this.state.selection]}`);
      socket.emit('question-response', {
        lectureId: this.state.lectureId,
        questionId: this.state.question.id,
        response: this.state.selection
      });
      this.setState({
        question: {},
        selection: -1
      });
    });
  }

  // Close socket on component dismount
  componentWillUnmount (): void {
    this.state.socket && this.state.socket.close();
  }

  // Handle lecture ID input change
  _onLectureIdChange = (event: Object): void => {
    this.setState({
      lectureId: event.target.value
    });
  }

  // Join the specified lecture
  _onJoinLecture = (lectureId: string): void => {
    if (this.state.currentLecture) return;
    if (!this.state.socket) return;
    axios.post('/api/v1/join-lecture', {
      socketId: this.state.socket.id,
      lectureId: lectureId
    }).then((response: Object) => {
      if (response.data.data.success) {
        console.log('Successfully joined lecture ' + lectureId);
        this.setState({
          currentLecture: lectureId
        });
      } else {
        alert(response.data.data.error);
      }
    }).catch((error: Object) => {
      console.log(error.message);
    });
  }

  _onQuestionSelect = (index: number): void => {
    this.setState({
      selection: index
    });
  }

  render (): React.Element<any> {
    return (
      <ClickerPage>
        {this.state.currentLecture && (
          <h4>
            {`In lecture: '${this.state.currentLecture}'`}
          </h4>
        )}
        <ClickerTextInput
          placeholder='Enter lecture id'
          value={this.state.lectureId}
          onChange={this._onLectureIdChange}
        />
        <ClickerButton
          onClick={ () => this._onJoinLecture(this.state.lectureId) }
          inverse={false}
          disabled={!this.state.lectureId} >
          Join Lecture
        </ClickerButton>
        {this.state.currentLecture &&
          (Object.keys(this.state.question).length !== 0) && (
            <ClickerQuestion
              data={this.state.question}
              onClick={this._onQuestionSelect}
              selection={this.state.selection}
            />
          )}
      </ClickerPage>
    );
  }
}

export default LectureStudent;
