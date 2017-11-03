// @flow
import React from 'React';
import axios from 'axios';
import io, {Socket} from 'socket.io-client';

import ClickerPage from '../common/ClickerPage';
import ClickerTextInput from '../common/ClickerTextInput';
import ClickerButton from '../common/ClickerButton';

type Props = {};
type State = {
  socket?: Socket,
  connected: boolean,
  courseId: string,
  lectureId: string
};

class LectureProfessor extends React.Component<Props, State> {
  props: Props;
  state: State;

  constructor (props: Props) {
    super(props);

    this.state = {
      socket: null,
      connected: false,
      courseId: '',
      lectureId: ''
    };
  }

  // Open socket and setup events on component mount
  componentDidMount (): void {
    const socket = io('/', {
      query: {
        userType: 'professor'
      }
    });

    this.setState({
      socket: socket
    });

    socket.on('connect', () => {
      console.log('Admin connected to socket');
      this.setState({
        connected: true
      });
    });

    socket.on('disconnect', () => {
      console.log('Admin disconnected from socket');
      this.setState({
        connected: false
      });
    });
  }

  // Close socket on component dismount
  componentWillUnmount (): void {
    this.state.socket && this.state.socket.close();
  }

  _onCourseIdChange = (event: Object): void => {
    this.setState({
      courseId: event.target.value
    });
  }

  _onLectureIdChange = (event: Object): void => {
    this.setState({
      lectureId: event.target.value
    });
  }

  // Start a new lecture given the course ID and current date
  _onStartLecture = (courseId: string): void => {
    if (this.state.lectureId) {
      alert('A lecture is already in session');
      return;
    }
    if (!this.state.socket) return;
    axios.post('/api/v1/start-lecture', {
      socketId: this.state.socket.id,
      courseId: courseId,
      date: (new Date()).toDateString()
    }).then((response: Object) => {
      if (response.data.data.success) {
        console.log(`Lecture started!
          Use lecture id '${response.data.data.lectureId}' to join`);
        this.setState({
          lectureId: response.data.data.lectureId
        });
      } else {
        console.log('Could not start lecture');
      }
    }).catch((error: Object) => {
      console.log('There was an error');
      console.log(error);
    });
  }

  // End a lecture given the lecture ID
  _onEndLecture = (): void => {
    if (!this.state.lectureId) {
      alert('No lecture currently in session');
      return;
    }
    if (!this.state.socket) return;
    const lectureId = this.state.lectureId;
    axios.post('/api/v1/end-lecture', {
      profId: this.state.socket.id,
      lectureId: lectureId
    }).then((response: Object) => {
      if (response.data.data) {
        console.log(`Lecture id '${lectureId}' was ended`);
        this.setState({
          lectureId: ''
        });
      } else {
        alert('Failed to end lecture with id "' + lectureId + '"');
      }
    }).catch((error: Object) => {
      console.log(error);
    });
  }

  // Start question - send to lecture participants
  // TODO: Put this functionality in QuestionCreator component
  _startQuestion = (): void => {
    console.log('sending question...');
    this.state.socket && this.state.socket.emit('question-start', {
      question: 'New Question!',
      choices: ['Armadillo', 'Beaver', 'Cheese'],
      answer: 0
    });
  }

  _endQuestion = (): void => {
    console.log('ending question...');
    this.state.socket && this.state.socket.emit('question-end');
  }

  render (): React.Element<any> {
    return (
      <ClickerPage>
        <ClickerTextInput
          placeholder='Enter course id'
          value={this.state.courseId}
          onChange={this._onCourseIdChange}
        />
        <ClickerButton
          onClick={ () => this._onStartLecture(this.state.courseId)}
          inverse={false}
          disabled={!this.state.courseId} >
          Start Lecture
        </ClickerButton>
        <ClickerButton
          onClick={this._onEndLecture}
          inverse={true}
          disabled={!this.state.lectureId} >
          End Lecture
        </ClickerButton>
        <ClickerButton
          onClick={this._startQuestion}
          inverse={false} >
          Start Question
        </ClickerButton>
        <ClickerButton
          onClick={this._endQuestion}
          inverse={true} >
          End Question
        </ClickerButton>
      </ClickerPage>
    );
  }
}

export default LectureProfessor;
