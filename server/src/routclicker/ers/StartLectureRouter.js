// @flow
import {Request} from 'express';
import AppDevRouter from '../utils/AppDevRouter';
import socket from 'socket.io';
import SocketServer from '../SocketServer';
import constants from '../utils/constants';

class StartLectureRouter extends AppDevRouter {
  constructor () {
    super(constants.REQUEST_TYPES.GET);
  }

  getPath (): string {
    return '/start-lecture/';
  }

  async content (req: Request) {
    // Start socket with namespace of id. (example: 4999) Statis for now.
    SocketServer.startLecture(4999);
    return 4999;
  }
}

export default new StartLectureRouter().router;
