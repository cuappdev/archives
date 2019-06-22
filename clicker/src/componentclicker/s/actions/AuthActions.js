// @flow
import AuthActionTypes from './AuthActionTypes';

import driver from '../common/driver';

const setSessionToken = (token: string) => {
  return {
    type: AuthActionTypes.SET_SESSION_TOKEN,
    token: token
  };
};

export default {
  setSessionToken
};
