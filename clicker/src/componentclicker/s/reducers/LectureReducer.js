// @flow
import LectureActionTypes from '../actions/LectureActionTypes';
import { QUESTION_TYPES } from '../common/constants';

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
  questionModalData: null,
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
      return {
        ...state,
        ...action.data,
        editLectureModalOpen: false
      };
    case LectureActionTypes.EDIT_QUESTION:
      return {
        ...state,
        questionModalOpen: true,
        questionModalData: action.data
      };
    case LectureActionTypes.CANCEL_EDIT_QUESTION:
      return {
        ...state,
        questionModalOpen: false,
        questionModalData: null
      };
    case LectureActionTypes.SAVE_QUESTION:
      if (action.status === 'success') {
        return {
          ...state,
          questions: action.questions,
          questionModalOpen: false
        };
      } else if (action.status === 'error') {
        // TODO: Possibly display error message
        console.log('Error on save question', action.error);
        return state;
      }
    default: return state;
  }
};

export default lectureReducer;
