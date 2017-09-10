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

  startLecture (id: number) {
    const nsp = this.io.of('/' + id);
    console.log('starting lecture');
    nsp.on('connection', sock => {
      console.log('someone connected to socket w id: ' + id);
    });
    nsp.emit('hi', 'yoyoyo');
  }

  on (action: string, callback: Function) {
    this.server.on(action, callback);
  }

  setupSocket (): void {
    this.io = socket(this.server);
    console.log('Socket.io listening on port', this.port);
    this.io.on('connection', this.onConnect);
  }

  onConnect = (client: Object): void => {
    console.log('Client connected to socket');
    client.on('disconnect', this.onDisconnect);
  };

  onDisconnect = (): void => {
    console.log('Client disconnected to socket');
  };
}

const instance = new SocketServer();

export default instance;
