import http from 'http';
import socket from 'socket.io';

/*

**SOCKET PROTOCOL**

bq: Begin Question
rq: Respond to Question
eq: End Question

sm: Send message

pc: Professor Count
sc: Student Count

*/

export default (app, port) => {

  const server = http.createServer(app);
  const io = socket(server);

  var question = null;
  var responses = {};
  var students = {};
  var professors = {};
  var messages = {};

  io.on('connection', (client) => {
    const address = client.handshake.address;
    const userType = client.handshake.query.userType;

    client.join(userType, () => {
      console.log(`Client has joined room: ${userType}`);
    });


    if (userType === 'professors') {
      professors[address] = (professors[address] || 0) + 1;

      client.emit('sm', { messages: messages });

      if (question) {
        client.emit('bq', { question: question });
        client.emit('rq', { responses: responses });
      }
    } else {
      students[address] = (students[address] || 0) + 1;

      if (question) {
        client.emit('bq', { question: question, response: responses[address] });
      }
    }

    io.emit('pc', Object.keys(professors).length);
    io.emit('sc', Object.keys(students).length);

    // Disconnect

    client.on('disconnect', () => {
      console.log(`Client disconnected with id: ${client.conn.id}`);

      if (userType === 'professors') {
        professors[address] -= 1;
        if (professors[address] === 0) delete professors[address];
        io.emit('pc', Object.keys(professors).length);
      } else {
        students[address] -= 1;
        if (students[address] === 0) delete students[address];
        io.emit('sc', Object.keys(students).length);
      }
    });

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

      question = null;
      responses = {};
      io.emit('eq');
    });

    // Students

    // Respond to Question
    client.on('rq', (data) => {
      console.log(`Student response received: ${data.response}`);

      responses[address] = data.response;

      let response = {};
      response[address] = data.response;
      io.to('professors').emit('rq', { responses: response });
    });

    // Message Professors
    client.on('sm', (data) => {
      console.log(`Incoming student message: ${data.message}`);

      messages[address] = data.message;

      let message = {};
      message[address] = data.message;
      io.to('professors').emit('sm', { messages: message });
    });

  });

  server.listen(port, () => {
    console.log('Clicker server listening on port ' + port);
  });
}