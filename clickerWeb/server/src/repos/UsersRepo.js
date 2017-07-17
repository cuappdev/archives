// @flow
import pool from './pool';
import Promise from 'bluebird';

const getUsersByCourse = (courseId: number): Promise<Array<Object>> => {
  return pool(`SELECT * FROM users where course_id = ${courseId}`)
    .then(rows => {
      return [];
    });
};

export default {
  getUsersByCourse
};
