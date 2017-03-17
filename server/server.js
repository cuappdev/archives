import express from 'express';
import path from 'path';
import utils from './utils';
import bodyParser from 'body-parser';

import lecture from './lecture';

/* Server */

const port = process.env.PORT || 3000;

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.use('/lecture/professor', utils.basicAuth('cuappdev', 'shipit'));
app.use(express.static(path.join(__dirname, '/../public')));

app.get('*', (req, res) => res.sendFile(path.join(__dirname, '/../public/index.html')));

lecture(app, port);
