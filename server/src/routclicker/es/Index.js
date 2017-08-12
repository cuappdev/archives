// @flow
import { Router, Request, Response, NextFunction } from 'express';
import UsersRepo from '../repos/UsersRepo';

class IndexRouter {
  router: Router;

  constructor () {
    this.router = new Router();
    this.init();
  }

  helloWorld (req: Request, res: Response, next: NextFunction) {
    res.json({ message: 'Hello, World' });
  }

  async users (req: Request, res: Response, next: NextFunction) {
    const rows = await UsersRepo.getUsers();
    res.json(rows);
  }

  init () {
    this.router.get('/test', this.helloWorld);
    this.router.get('/users', this.users);
  }
}

const indexRouter = new IndexRouter();
export default indexRouter.router;
