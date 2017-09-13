// @flow
import express, { Request, Response, NextFunction } from 'express';
import bodyParser from 'body-parser';
import path from 'path';
import serveFavicon from 'serve-favicon';

// All routers
import GetUsersRouter from './routers/GetUsersRouter';
import GoogleSignInRouter from './routers/GoogleSignInRouter';
import GetMeRouter from './routers/GetMeRouter';
import StartLectureRouter from './routers/StartLectureRouter';

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
    this.express.use(serveFavicon(path.join(__dirname, '../public/favicon.ico')));
  }

  site = (req: Request, res: Response, next: NextFunction): void => {
    res.sendFile('index.html', { root: path.join(__dirname, '../public') });
  };

  _use (Router: any): void {
    this.express.use('/api/v1', Router);
  }

  routes (): void {
    // Load all them routers
    this._use(GetUsersRouter);
    this._use(GoogleSignInRouter);
    this._use(GetMeRouter);
    this._use(StartLectureRouter);

    // Front-end files
    this.express.use(express.static(path.join(__dirname, '../public')));
    this.express.get('*', this.site);
  }
}

export default API;
