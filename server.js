import express from 'express';
import path from 'path';

const port = process.env.PORT || 3000;
const app = express();

app.use(express.static(__dirname + '/public'));

app.get('*', (request, response) => {
  response.sendFile(path.resolve(__dirname, 'public', 'index.html'))
})

app.listen(port, () => {
  console.log ("Clicker started on port " + port);
});
