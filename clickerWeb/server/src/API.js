// @flow
import express, { Request, Response, NextFunction } from 'express';
import bodyParser from 'body-parser';
import path from 'path';

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
    this.express.use(bodyParser.urlencoded({ extended: false }));
  }

  site = (req: Request, res: Response, next: NextFunction): void => {
    res.sendFile(path.join(__dirname, '../public/index.html'));
  };

  routes (): void {
    this.express.use('/api/v1/', IndexRouter);
    this.express.use('/api/v1/classes/', ClassesRouter);

    // Front-end files
    this.express.use(express.static(path.join(__dirname, '../public')));
    this.express.get('*', this.site);
  }
}

export default API;
