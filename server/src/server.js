// @flow
import API from './API';

import dbConnection from './db/DbConnection';
import http from 'http';
import SocketServer from './SocketServer';

type Error = {
  errno?: number;
  code?: string;
  path?: string;
  syscall?: string;
};

const app: API = new API();
const port: number = 3000;
const server: http.Server = http.createServer(app.express);

const onError = (error: Error): void => {
  if (error.syscall !== 'listen') throw error;
  switch (error.code) {
  case 'EACCES':
    console.error(`${port} requires elevated privileges`);
    process.exit(1);
  case 'EADDRINUSE':
    console.error(`${port} is already in use`);
    process.exit(1);
  default:
    throw error;
  }
};

const onListening = (): void => {
  let addr: Object = server.address();
  console.log(`Listening on ${addr.port}`);
};

<<<<<<< HEAD
// Configures server
SocketServer.server = server;
SocketServer.port = port;
SocketServer.runServer();
SocketServer.on('error', onError);
SocketServer.on('listening', onListening);
SocketServer.setupSocket();
=======
const mountApp = (): void => {
  const socketServer = new SocketServer(server, port);
  socketServer.runServer();
  socketServer.on('error', onError);
  socketServer.on('listening', onListening);
  socketServer.setupSocket();
};

// Bootstrap everything
dbConnection().then(_ => {
  mountApp();
}).catch(err => {
  console.log(err);
});
>>>>>>> origin/master
