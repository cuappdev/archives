// @flow
import pool from './pool';

const getUsers = async (): Promise<Array<Object>> => {
  const rows = await pool('SELECT * FROM users');
  return rows;
};

export default {
  getUsers
};
