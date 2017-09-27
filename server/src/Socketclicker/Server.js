// @flow
import http from 'http';
import socket from 'socket.io';

class SocketServer {
  server: http.Server;
  port: number;
  io: Object;
  lectures: Object;

  constructor() {
    this.lectures = {};
  }

  runServer (): void {
    this.server.listen(this.port);
  }

  on (action: string, callback: Function) {
    this.server.on(action, callback);
  }

  setupSocket (): void {
    this.io = socket(this.server);
    console.log('Socket.io listening on port', this.port);
    this.io.on('connect', this._onConnect);
  }

  // Handle client socket connection
  _onConnect = (client: Object): void => {
    const clientId = client.id;
    const userType = client.handshake.query.userType;

    if (userType === 'professor') {
      console.log(`Professor with id ${clientId} connected to socket`);
      this._setupProfessorEvents(client);
    } else {
      console.log(`Student with id ${clientId} connected to socket`);
      const netId = client.handshake.query.netId;
      this._setupStudentEvents(client);
    }

    // Handle client socket disconnection
    client.on('disconnect', () => {
      if (userType === 'professor') {
        console.log(`Professor with id ${client.id} disconnected from socket`);
      } else {
        console.log(`Student with id ${client.id} disconnected from socket`);
      }
    });
  };

  _setupProfessorEvents = (client: Object): void => {
    const address = client.handshake.address;

  }

  _setupStudentEvents = (client: Object): void => {
    const address = client.handshake.address;
    const netId = client.handshake.query.netid;
  }

  // Start lecture with namespace of lecture id
  startLecture(profId: string, lectureId: string): boolean {
    if (this.lectures[lectureId]) {
      console.log('This lecture is already in session');
      return false;
    }
    console.log('STARTING lecture with namespace: /' + lectureId);
    const nsp = this._createNamespace(lectureId);
    this.lectures[lectureId] = {
      professor: profId,
      students: {}
    };
    console.log(this.lectures);

    nsp.on('connection', (client) => {
      var success = this.joinLecture(client, lectureId);
      if (success) {
        socket.emit('welcome', `Welcome to lecture ${lectureId}!`)
      };
    });

    return true;
  }

  // End lecture by disconnecting client sockets and removing namespace
  endLecture = (profId: string, lectureId: string): boolean => {
    try {
      const lecture = this.lectures[lectureId];
      if (!lecture) {
        throw new Error('No lecture with id /' + lectureId);
      }
      if (lecture.professor !== profId) {
        throw new Error('Professor lacks permission to end lecture /' + lectureId);
      }
      const nsp = this._getNamespace(lectureId);
      console.log('ENDING lecture with namespace: /' + lectureId);
      Object.values(nsp.connected).forEach((socket) => {
        socket.close();
      });
      this._deleteNamespace(lectureId);
      delete this.lectures[lectureId];
    } catch (error) {
      console.log(error.message);
      return false;
    }
    return true;
  }

  // Client socket joins the specified lecture if validated,
  // disconnects otherwise
  joinLecture = (client: Object, lectureId: string): boolean => {
    var isValid = this._validateUser(client);
    if (!isValid) {
      client.disconnect();
    } else {
      console.log(`Student ${client.id} joined lecture ${lectureId}`);
      client.on('disconnect', () => this.leaveLecture(client, lectureId));
    }
    return isValid;
  }

  leaveLecture = (client: Object, lectureId: string): void => {
    const students = this.lectures[lectureId].students;
    delete students[client.id];
    this.lectures[lectureId] = {
      ...this.lectures[lectureId],
      students: students
    }
    console.log(`Student ${client.id} left lecture ${lectureId}`);
  }

  _validateUser = (user: Object): boolean => {
    // TODO - Validate this user
    return true;
  }

  // Creates and returns a namespace object
  _createNamespace = (name: string): Object => {
    const nsp = this.io.of('/' + name);
    return nsp;
  }

  // Returns a namespace object if it exists, otherwise throws and error
  _getNamespace = (name: string): Object => {
    const nsp = this.io.nsps['/' + name];
    if (!nsp) {
      throw new Error('Namespace /' + name + ' not found.');
    }
    return nsp;
  }

  // Deletes a namespace if it exists
  _deleteNamespace = (name: string): boolean => {
    var success = delete this.io.nsps['/' + name];
    return success;
  }
}

const socketServer = new SocketServer();

export default socketServer;
