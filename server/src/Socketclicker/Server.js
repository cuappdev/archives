// @flow
import http from 'http';
import socket from 'socket.io';

class SocketServer {
  server: http.Server;
  port: number;
  io: Object;

  runServer (): void {
    this.server.listen(this.port);
  }

  on (action: string, callback: Function) {
    this.server.on(action, callback);
  }

  setupSocket (): void {
    this.io = socket(this.server);
    console.log('Socket.io listening on port', this.port);
    this.io.on('connection', this._onConnect);
  }

  _onConnect = (client: Object): void => {
    console.log('Client '+client.id+' connected to server socket');
    client.on('disconnect', () => this._onDisconnect(client));
  };

  _onDisconnect = (client: Object): void => {
    console.log('Client '+client.id+' disconnected from server socket');
  };

  // Start lecture with namespace of lecture id
  startLecture = (id: string) => {
    console.log('STARTING lecture with namespace: /' + id);
    const nsp = this._createNamespace(id);
    nsp.on('connection', (socket) => {
      var success = this.joinLecture(socket, id);
      if (success) {
        socket.emit('welcome', `Welcome to lecture ${id}!`)
      };
    });
  }

  // End lecture by disconnecting client sockets and removing namespace
  endLecture = (id: string): boolean => {
    try {
      const nsp = this._getNamespace(id);
      console.log('ENDING lecture with namespace: /' + id);
      Object.values(nsp.connected).forEach((socket) => {
        socket.disconnect();
      });
      this._deleteNamespace(id);
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
      console.log(client.id + ' joined lecture ' + lectureId);
      client.on('disconnect', () => this.leaveLecture(client, lectureId));
    }
    return isValid;
  }

  leaveLecture = (client: Object, lectureId: string): void => {
    console.log(client.id + ' left lecture ' + lectureId);
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
