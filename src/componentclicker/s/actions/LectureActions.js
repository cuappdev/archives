// @flow
import LectureActionTypes from './LectureActionTypes';
import axios from 'axios';

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
  };
};

const editQuestion = (data?: Object) => {
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

const saveQuestionSuccess = (questions: Array<Object>) => {
  return {
    type: LectureActionTypes.SAVE_QUESTION,
    status: 'success',
    questions: questions
  };
};

const saveQuestionFailure = (error: Object) => {
  return {
    type: LectureActionTypes.SAVE_QUESTION,
    status: 'error',
    error: Object
  };
};

const saveQuestion = (data: Object) =>
(dispatch: Function, getState: Function) => {
  const formattedData = {
    type: data.questionType,
    text: data.questionText,
    data: { ...data.data }
  };
  console.log(formattedData);

  if (data.questionId) {
    // Update question
    // TODO
  } else {
    // Create new question
    // TODO: Include lecture id as parameter
    const lectureId = 1;
    axios.post(`/api/v1/lectures/${lectureId}/questions`, {
      type: data.questionType,
      text: data.questionText,
      data: JSON.stringify({ ...data.data })
    }).then(response => {
      if (response.data.success) {
        // TODO: Fetch updated questions for lectureId & update store
        const questions = getState().lecture.questions;
        questions.push(response.data.data.node);
        dispatch(saveQuestionSuccess(questions));
      } else {
        dispatch(saveQuestionFailure(response.data.data));
      }
    }).catch(error => {
      console.log('Server Error', error);
    });
  }
};

const deleteQuestion = (id: number) =>
(dispatch: Function, getState: Function) => {
  // TODO: Delete this question and dispatch actions appropriately
  console.log('Deleting question with id ' + id);
};

export default {
  toggleEditModal,
  saveLecture,
  toggleQuestionModal,
  editQuestion,
  cancelEditQuestion,
  saveQuestion,
  deleteQuestion
};
