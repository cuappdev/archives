// @flow
import keyMirror from 'keymirror';

const LectureActionTypes = keyMirror({
  TOGGLE_EDIT_MODAL: null,
  SAVE_LECTURE: null,
  EDIT_QUESTION: null,
  CANCEL_EDIT_QUESTION: null,
  SAVE_QUESTION: null
});

export default LectureActionTypes;
