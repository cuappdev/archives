// @flow
import LectureActionTypes from './LectureActionTypes';

const toggleEditModal = (show: boolean) => {
  return {
    type: LectureActionTypes.TOGGLE_EDIT_MODAL,
    show: show
  };
};

// TODO: Make this a thunk
const saveLecture = (data: Object) => {
  return {
    type: LectureActionTypes.SAVE_LECTURE,
    data: data
  };
};

const toggleQuestionModal = (show: boolean) => {
  return {
    type: LectureActionTypes.TOGGLE_QUESTION_MODAL,
    show: show
  }
}

const editQuestion = (data: Object) => {
  console.log('Edit question', data);
  return {
    type: LectureActionTypes.EDIT_QUESTION,
    data: data
  };
};

const cancelEditQuestion = () => {
  return {
    type: LectureActionTypes.CANCEL_EDIT_QUESTION
  };
};

const saveQuestionSuccess = (response: Object) => {
  return {
    type: LectureActionTypes.SAVE_QUESTION,
    status: 'success',
    response: response
  };
};

const saveQuestionFailure = (error: string) => {
  return {
    type: LectureActionTypes.SAVE_QUESTION,
    status: 'error',
    error: error
  }
}

const saveQuestion = (data: Object) =>
(dispatch: Function, getState: Function) => {
  // TODO: Save question and return success or not
  // for now, update lecture state with new question
  const questions = getState().lecture.questions;
  if (data.questionId) {

  } else {
    questions.push({
      ...data,
      questionId: questions.length
    });
  }
  dispatch(saveQuestionSuccess(questions))
};

export default {
  toggleEditModal,
  saveLecture,
  toggleQuestionModal,
  editQuestion,
  cancelEditQuestion,
  saveQuestion
};
