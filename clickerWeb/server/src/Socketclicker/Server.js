// @flow
import http from 'http';
import socket from 'socket.io';

class SocketServer {
  server: http.Server;
  port: number;
  io: Object;

  constructor (server: http.Server, port: number) {
    this.server = server;
    this.port = port;
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

export default SocketServer;
