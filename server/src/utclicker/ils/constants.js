// flow

export type RequestType = 'POST' | 'GET' | 'DELETE';

const REQUEST_TYPES = {
  POST: 'POST',
  GET: 'GET',
  DELETE: 'DELETE'
};

const QUESTION_TYPES = {
  MULTIPLE_CHOICE: 'MULTIPLE_CHOICE',
  FREE_RESPONSE: 'FREE_RESPONSE',
  CHECKBOX: 'CHECKBOX',
  RANKING: 'RANKING'
};

export default {
  REQUEST_TYPES,
  QUESTION_TYPES
};
