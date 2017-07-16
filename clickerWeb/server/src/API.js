// @flow
import bodyParser from 'body-parser';
import express from 'express';

import ClassesRouter from './routes/Classes';
import IndexRouter from './routes/Index';

class API {
  express: Object;

  constructor () {
    this.express = express();
    this.middleware();
    this.routes();
  }

  middleware (): void {
    this.express.use(bodyParser.json());
    this.express.use(bodyParser.urlencoded({extended: false}));
  }

  routes (): void {
    this.express.use('/api/v1/', IndexRouter);
    this.express.use('/api/v1/classes/', ClassesRouter);
  }
}

export default API;
