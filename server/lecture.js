import http from 'http';
import socket from 'socket.io';

export default (app, port) => {

  const server = http.createServer(app);
  const io = socket(server);

  var question = null;
  var responses = {};
  var clients = [];

  io.on('connection', (client) => {
    const address = client.handshake.address;
    const userType = client.handshake.query.userType;

    client.join(userType, () => {
      console.log(`Client has joined room: ${userType}`);
    });

    if (userType === 'professors') {
      client.emit('bq', { question: question });
      client.emit('rq', { responses: responses });
    } else {
      client.emit('bq', { question: question, response: responses[address] });
    }

    // Professors

    // Begin Question
    client.on('bq', (data) => {
      console.log(`Beginning question: ${data.question.text}`);

      question = data.question
      io.emit('bq', data);
    });

    // End Question
    client.on('eq', () => {
      console.log('Question ended');

      question = null
      responses = {}
      io.emit('eq');
    });

    // Students

    // Respond to Question
    client.on('rq', (data) => {
      console.log(`Student response received: ${data.response}`);

      responses[address] = data.response;

      var response = {}
      response[address] = data.response
      io.to('professors').emit('rq', data);
    });

    // Ping Professors
    client.on('pp', (data) => {
      console.log(`Professor pinged: ${data.ping.text}`);
      io.to('professors').emit('pp', data);
    });

    client.on('disconnect', () => {
      console.log(`Client disconnected with id: ${client.conn.id}`);
    });
  });

  server.listen(port, () => {
    console.log('Clicker server listening on port ' + port);
  });
}
