// @flow
import { Router } from 'express';

class ClassesRouter {
  router: Router;

  constructor () {
    this.router = new Router();
    this.init();
  }

  init () {} // TODO
}

const classesRouter = new ClassesRouter();
export default classesRouter.router;
