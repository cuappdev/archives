// @flow
import Model from './Model';

export type UserFields = {
  id?: string;
  googleId: string;
  netId: string;
  firstName: string;
  lastName: string;
  email: string;
  createdAt?: Date;
  updatedAt?: Date;
};

class User extends Model {
  fields: UserFields;
}

export default User;
