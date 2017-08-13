// @flow
import { Request } from 'express';
import AppDevRouter from '../utils/AppDevRouter';

import appDevUtils from '../utils/appDevUtils';

class GetMeRouter extends AppDevRouter {
  constructor () {
    super('POST');
  }

  getPath (): string {
    return '/users/me/';
  }

  async content (req: Request) {
    const accessToken = req.query.access_token;
    const params = {
      access_token: accessToken,
      alt: 'json'
    };
    const uri = `/oauth2/v1/userinfo?${appDevUtils.encodeUrlParams(params)}`;

    // Grab JSON info about the user from Google
    const googleResponse = await appDevUtils.googleAxios.get(uri);

    // TODO -> check to see if user exists with this information,
    // if a user exists, return that user, if not, make that user and return
    // that user

    return googleResponse.data;
  }
}

export default new GetMeRouter().router;
