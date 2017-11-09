// @flow
import keyMirror from 'keymirror';

const COLORS = {
  OFF_WHITE: '#F5F5F5',
  WHITE: '#FFFFFF',
  LIGHT_GRAY: '#D3D3D3D3',
  GRAY: '#A9A9A9',
  DARK_GRAY: '#696969',
  BLACK: '#000000',
  GREEN: '#55C94C',
  FONT_FAMILY: '"Trebuchet MS", Helvetica, sans-serif'
};

export type QuestionType = 'MULTIPLE_CHOICE' | 'FREE_RESPONSE' |
  'MULTIPLE_ANSWER' | 'RANKING'

const QUESTION_TYPES = {
  MULTIPLE_CHOICE: 'MULTIPLE_CHOICE',
  FREE_RESPONSE: 'FREE_RESPONSE',
  MULTIPLE_ANSWER: 'MULTIPLE_ANSWER',
  RANKING: 'RANKING'
};
// const QUESTION_TYPES = keyMirror({
//   MULTIPLE_CHOICE: null,
//   FREE_RESPONSE: null,
//   MULTIPLE_ANSWER: null,
//   RANKING: null
// });

export {
  QUESTION_TYPES,
  COLORS
}
