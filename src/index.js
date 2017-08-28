import express from 'express';
import path from 'path';
import basicAuth from './basicAuth';

import lecture from './lecture.js';
import dotenv from 'dotenv';
dotenv.config();

/* Server */

const port = process.env.PORT || 3000;

const app = express();

app.use(express.static(path.join(__dirname, '/../public')));

app.get('/lecture/professor', basicAuth, (req, res) => res.sendFile(path.join(__dirname, '/../public/index.html')));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, '/../public/index.html')));

lecture(app, port);
