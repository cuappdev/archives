// @flow
import {
  getConnectionManager,
  Repository,
  json
} from 'typeorm';
import {Question} from '../models/Question';
import {QUESTION_TYPE} from '../utils/constants';
import LecturesRepo from './LecturesRepo';

const db = (): Repository<Question> => {
  return getConnectionManager().get().getRepository(Question);
};

// Create a question
const createQuestion = async (text: string, type: QUESTION_TYPE,
  data: json, lectureId: number): Promise<Question> => {
  try {
    const question = new Question();
    question.text = text;
    question.type = type;
    question.data = data;
    question.lecture = await LecturesRepo.getLectureById(lectureId);
    await db().persist(question);
    return question;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating question!');
  }
};

// Get a question by Id
const getQuestionById = async (id: number): Promise<?Question> => {
  try {
    const question = await db().findOneById(id);
    return question;
  } catch (e) {
    throw new Error(`Problem getting question by id: ${id}!`);
  }
};

// Get questions
const getQuestions = async (): Promise<Array<Question>> => {
  try {
    const questions = await db().createQueryBuilder('questions')
      .getMany();
    return questions;
  } catch (e) {
    throw new Error('Problem getting questions!');
  }
};

export default {
  createQuestion,
  getQuestionById,
  getQuestions
};
