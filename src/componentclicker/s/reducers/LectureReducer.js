// @flow
import LectureActionTypes from '../actions/LectureActionTypes';

export type LectureState = {
  id?: number,
  title?: string,
  date?: string,
  questions: Array<Object>
};

const initialState: LectureState = {
  lectureTitle: 'New Lecture',
  editLectureModalOpen: false,
  questionModalOpen: false,
  questions: []
};

let lectureReducer = (
  state: LectureState = initialState,
  action: Object
): LectureState => {
  switch (action.type) {
    case LectureActionTypes.TOGGLE_EDIT_LECTURE_MODAL:
      return {
        ...state,
        editLectureModalOpen: action.show
      }
    case LectureActionTypes.EDIT_LECTURE_SAVE:
      console.log('Edit lecture save', action);
      return {
        ...state,
        ...action.data,
        editLectureModalOpen: false
      }
    case LectureActionTypes.TOGGLE_QUESTION_MODAL:
      return {
        ...state,
        questionModalOpen: action.show
      }
    case LectureActionTypes.LECTURE_QUESTION_SAVE:
      return {
        ...state
      }
    default: return state;
  }
};

export default lectureReducer;
