// @flow
import { Request } from 'express';
import AppDevRouter from '../utils/AppDevRouter';
import UsersRepo from '../repos/UsersRepo';

import appDevUtils from '../utils/appDevUtils';

class GetMeRouter extends AppDevRouter {
  constructor () {
    super('POST');
  }

  getPath (): string {
    return '/users/me/';
  }

  async content (req: Request) {
    const accessToken = req.query.accessToken;
    const params = {
      access_token: accessToken,
      alt: 'json'
    };
    const uri = `/oauth2/v1/userinfo?${appDevUtils.encodeUrlParams(params)}`;

    // Grab JSON info about the user from Google
    const googleResponse = await appDevUtils.googleAxios.get(uri);
    const data = googleResponse.data;

    // Check if user exists, if not make a new one
    let user = await UsersRepo.getUserByGoogleId(data['id']);
    if (!user) {
      user = await UsersRepo.createUser({
        googleId: data['id'],
        netId: appDevUtils.netIdFromEmail(data['email']),
        firstName: data['given_name'],
        lastName: data['family_name'],
        email: data['email']
      });
    }

    return user;
  }
}

export default new GetMeRouter().router;
