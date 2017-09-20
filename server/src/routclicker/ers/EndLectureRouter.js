// @flow
import {Request} from 'express';
import AppDevRouter from '../utils/AppDevRouter';
import socket from 'socket.io';
import SocketServer from '../SocketServer';
import constants from '../utils/constants';

class EndLectureRouter extends AppDevRouter {
  constructor () {
    super(constants.REQUEST_TYPES.GET);
  }

  getPath (): string {
    return '/end-lecture/';
  }

  async content (req: Request) {
    // Close socket with namespace of lectureId
    const lectureId = req.query.lectureId;
    const success = SocketServer.endLecture(lectureId);
    return success;
  }
}

export default new EndLectureRouter().router;
