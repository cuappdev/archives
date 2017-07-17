// @flow
import pool from './pool';
import Promise from 'bluebird';

const getUsers = (): Promise<Array<any>> => {
  return pool('SELECT * FROM users')
    .then(rows => {
      return rows;
    });
};

export default {
  getUsers
};
