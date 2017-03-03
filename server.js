import http from 'http';
import express from 'express';
import path from 'path';
import socket from 'socket.io';

/* Server */

const port = process.env.PORT || 8008;
const app = express();

app.use(express.static(__dirname + '/public'));

app.get('*', (req, res) => res.sendFile(path.resolve(__dirname, 'public', 'index.html'))).listen(port, () => {
  console.log('Started Clicker server on port ' + port);
});

/* Sockets */

const server = http.createServer(app);
const io = socket(server);
const socketPort = 3000;

io.on('connection', (client) => {
  console.log(`Client connected with id: ${client.conn.id}`);
  const userType = client.handshake.query.userType;

  client.join(userType, () => {
    console.log(`Client has joined room: ${userType}`);
  });

  // Professors

  // Begin Question
  client.on('bq', (data) => {
    console.log(`Beginning question: ${data.text}`);
    io.emit('bq', data);
  });

  // End Question
  client.on('eq', (data) => {
    console.log('Question ended');
    io.emit('eq', data);
  });

  // Students

  // Respond to Question
  client.on('rq', (data) => {
    console.log(`Student response received: ${data}`);
    io.to('professors').emit('rq', data);
  });

  // Ping Professors
  client.on('pp', (data) => {
    console.log(`Professor pinged: ${data.text}`);
    io.to('professors').emit('pp', data);
  });

  client.on('disconnect', () => {
    console.log(`Client disconnected with id: ${client.conn.id}`);
  });
});

server.listen(socketPort, () => {
  console.log('Listening for socket.io connections on port ' + socketPort);
});