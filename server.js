import http from 'http';
import express from 'express';
import path from 'path';
import socket from 'socket.io';

const port = process.env.PORT || 8008;
const app = express();

app.use(express.static(__dirname + '/public'));

app.get('*', (request, response) => {
  response.sendFile(path.resolve(__dirname, 'public', 'index.html'))
});

const server = http.createServer(app);
const io = socket(server);
const socketPort = 3000;

io.on('connection', (client) => {
  console.log(`Client connected with id: ${client.conn.id}`);

  client.on('event', (data) => {

  });

  client.on('disconnect', () => {
    console.log(`Client disconnected with id: ${client.conn.id}`);
  });
});

server.listen(socketPort, () => {
  console.log ('Listening for socket.io connections on port ' + socketPort);
});

app.listen(port, () => {
  console.log('Started Clicker server on port ' + port);
});