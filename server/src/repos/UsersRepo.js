// @flow
import type { UserFields } from '../models/User';

import User from '../models/User';

import appDevUtils from '../utils/appDevUtils';
import pool from './pool';

const createUser = async (fields: UserFields): Promise<User> => {
  const user = new User(fields);
  const insertStatement = appDevUtils.insertIntoMySQLStatement(
    'users',
    user.fields
  );
  const okPacket = await pool(insertStatement);
  const createdUser = await getUserById(okPacket['insertId']);

  if (!createdUser) throw new Error('Problem creating user');
  return createdUser;
};

const getUserById = async (id: number): Promise<?User> => {
  const rows = await pool(`SELECT * FROM users WHERE id=${id}`);
  return rows.length > 0 ? new User(rows[0]) : null;
};

const getUserByGoogleId = async (googleId: string): Promise<?User> => {
  const rows = await pool(`SELECT * FROM users WHERE googleId='${googleId}'`);
  return rows.length > 0 ? new User(rows[0]) : null;
};

const getUsers = async (): Promise<Array<Object>> => {
  const rows = await pool('SELECT * FROM users');
  return rows;
};

export default {
  getUsers,
  createUser,
  getUserById,
  getUserByGoogleId
};
