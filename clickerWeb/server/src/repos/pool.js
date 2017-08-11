// @flow
import mysql from 'mysql';

const pool = mysql.createPool({
  connectionLimit: 10,
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DB,
  debug: true
});

const useDB = (query: string): Promise<any> => {
  return new Promise((resolve, reject) => {
    pool.getConnection((err: Object, connection) => {
      if (err) {
        reject(err);
      }
      connection.query(query, (err: Object, rows) => {
        if (err) {
          reject(err);
        }
        return rows;
      });
    });
  });
};

export default useDB;
