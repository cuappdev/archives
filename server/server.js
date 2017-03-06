import http from 'http';
import express from 'express';
import path from 'path';
import socket from 'socket.io';
import utils from './utils';
import bodyParser from 'body-parser';

/* Server */

const port = process.env.PORT || 3000;

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.use('/lecture/professor', utils.basicAuth('cuappdev', 'shipit'));
app.use(express.static(path.join(__dirname, '/../public')));

app.post('/login', (req, res) => {
  res.status(200).json({
    success: true
    // success: req.body.password === 'shipit'
  });
});

app.get('*', (req, res) => res.sendFile(path.join(__dirname, '/../public/index.html')));

/* Sockets */

const server = http.createServer(app);
const io = socket(server);

var question = null
var responses = {}
var clients = []

io.on('connection', (client) => {
  const address = client.handshake.address;
  const userType = client.handshake.query.userType;

  client.emit('bq', question);

  if (userType === 'professors') {
    console.log(responses);
    client.emit('rq', responses);
  }

  client.join(userType, () => {
    console.log(`Client has joined room: ${userType}`);
  });

  // Professors

  // Begin Question
  client.on('bq', (data) => {
    console.log(`Beginning question: ${data.text}`);

    question = data
    io.emit('bq', data);
  });

  // End Question
  client.on('eq', (data) => {
    console.log('Question ended');

    question = null
    responses = {}
    io.emit('eq', data);
  });

  // Students

  // Respond to Question
  client.on('rq', (data) => {
    console.log(`Student response received: ${data}`);

    responses[address] = data;

    var response = {}
    response[address] = data
    io.to('professors').emit('rq', response);
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

server.listen(port, () => {
  console.log('Clicker server listening on port ' + port);
});
