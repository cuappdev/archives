// @flow
import { getConnectionManager, Repository } from 'typeorm';
import { User } from '../models/User';

const db = (): Repository<User> => {
  return getConnectionManager().get().getRepository(User);
};

// Create a user with fields
const createUser = async (fields: Object): Promise<User> => {
  try {
    const user = await db().persist(User.fromGoogleCreds(fields));
    return user;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating user!');
  }
};

// Get a user by Id
const getUserById = async (id: number): Promise<?User> => {
  try {
    const user = await db().findOneById(id);
    return user;
  } catch (e) {
    throw new Error(`Problem getting user by id: ${id}!`);
  }
};

// Get a user by googleId (a.k.a. unique key of their Google account)
const getUserByGoogleId = async (googleId: string): Promise<?User> => {
  try {
    const user = await db().createQueryBuilder('users')
      .where('users.googleId = :googleId', { googleId: googleId })
      .getOne();
    return user;
  } catch (e) {
    throw new Error('Problem getting user by google ID!');
  }
};

// Get users
const getUsers = async (): Promise<Array<User>> => {
  try {
    const users = await db().createQueryBuilder('users')
      .getMany();
    return users;
  } catch (e) {
    throw new Error('Problem getting users!');
  }
};

export default {
  getUsers,
  createUser,
  getUserById,
  getUserByGoogleId
};
