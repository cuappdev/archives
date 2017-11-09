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
  }
}

const editQuestion = (data?: Object) => {
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

const saveQuestionSuccess = (questions: Array<Object>) => {
  return {
    type: LectureActionTypes.SAVE_QUESTION,
    status: 'success',
    questions: questions
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
    axios.post('/api/v1/lectures/1/questions', {
      type: data.questionType,
      text: data.questionText,
      data: JSON.stringify({ ...data.data })
    }).then(response => {
      console.log(response);
      if (response.data.success) {
        const questions = getState().lecture.questions;
        console.log('Questions', questions);
        questions.push(response.data.data.node);
        dispatch(saveQuestionSuccess(questions));
      } else {
        console.log(response.data.data);
      }
    }).catch(error => {
      console.log(error);
    });
  }
};

export default {
  toggleEditModal,
  saveLecture,
  toggleQuestionModal,
  editQuestion,
  cancelEditQuestion,
  saveQuestion
};
