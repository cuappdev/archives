// @flow
import AuthActionTypes from '../actions/AuthActionTypes';

export type AuthState = {
  sessionToken: ?string
};

const initialState: AuthState = {
  sessionToken: null
};

let auth = (
  state: AuthState = initialState,
  action: Object
): AuthState => {
  switch (action.type) {
  case AuthActionTypes.SET_SESSION_TOKEN:
    return {
      ...state,
      sessionToken: action.token
    };
  default: return state;
  }
};

export default auth;
