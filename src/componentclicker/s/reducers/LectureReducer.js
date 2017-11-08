// @flow
import LectureActionTypes from '../actions/LectureActionTypes';

export type LectureState = {
  id?: number,
  lectureTitle: string,
  lectureDate?: string,
  editLectureModalOpen: boolean,
  questionModalOpen: boolean,
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
    case LectureActionTypes.TOGGLE_EDIT_MODAL:
      return {
        ...state,
        editLectureModalOpen: action.show
      };
    case LectureActionTypes.SAVE_LECTURE:
      console.log('Edit lecture save', action);
      return {
        ...state,
        ...action.data,
        editLectureModalOpen: false
      };
    case LectureActionTypes.EDIT_QUESTION:
      return {
        ...state,
        ...action.data,
        questionModalOpen: true
      };
    case LectureActionTypes.CANCEL_EDIT_QUESTION:
      return {
        ...state,
        questionModalOpen: false
      }
    case LectureActionTypes.SAVE_QUESTION:
      // TODO: Fix
      console.log('SAVE_QUESTION', action);
      return {
        ...state,
        questionModalOpen: false
      };
    default: return state;
  }
};

export default lectureReducer;
