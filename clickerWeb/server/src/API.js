// @flow

import bodyParser from 'body-parser';
import express from 'express';

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
    this.express.use((req: Object, res: Object) => {
      res.json({
        message: 'Hello, World!'
      });
    });
  }
}

export default API;
