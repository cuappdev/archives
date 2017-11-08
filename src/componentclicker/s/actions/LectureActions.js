// @flow
import LectureActionTypes from './LectureActionTypes';

const toggleEditLectureModal = (show: boolean) => {
  return {
    type: LectureActionTypes.TOGGLE_EDIT_LECTURE_MODAL,
    show: show
  };
};

const editLectureSave = (data: Object) => {
  return {
    type: LectureActionTypes.EDIT_LECTURE_SAVE,
    data: data
  };
};

const toggleQuestionModal = (show: boolean) => {
  return {
    type: LectureActionTypes.TOGGLE_QUESTION_MODAL,
    show: show
  }
}

const lectureQuestionSave = (data: Object) => {
  return {
    type: LectureActionTypes.LECTURE_QUESTION_SAVE,
    data: data
  };
};

export default {
  toggleEditLectureModal,
  editLectureSave,
  toggleQuestionModal,
  lectureQuestionSave
};
