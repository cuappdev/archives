// @flow
import {
  getConnectionManager,
  Repository,
  json
} from 'typeorm';
import {Response} from '../models/Response';
import {QUESTION_TYPE} from '../utils/constants';
import QuestionsRepo from './QuestionsRepo';
import UsersRepo from './UsersRepo';

const db = (): Repository<Response> => {
  return getConnectionManager().get().getRepository(Response);
};

// Create a response
const createResponse = async (type: QUESTION_TYPE, data: json,
  questionId: number, userId: number): Promise<Response> => {
  try {
    const response = new Response();
    response.type = type;
    response.response = data;
    response.question = await QuestionsRepo.getQuestionById(questionId);
    response.user = await UsersRepo.getUserById(userId);
    await db().persist(response);
    return response;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating response!');
  }
};

// Get a response by Id
const getResponseById = async (id: number): Promise<?Response> => {
  try {
    const response = await db().findOneById(id);
    return response;
  } catch (e) {
    throw new Error(`Problem getting response by id: ${id}!`);
  }
};

// Get responses
const getResponses = async (): Promise<Array<Response>> => {
  try {
    const responses = await db().createQueryBuilder('responses')
      .getMany();
    return responses;
  } catch (e) {
    throw new Error('Problem getting questions!');
  }
};

// Get responses by question id
const getResponsesByQuestionId = async (questionId: number): Promise<Array<Response>> => {
  try {
    const responses = await db().createQueryBuilder('responses')
      .innerJoinAndSelect("responses.question", "question")
      .where("question.id=:questionId")
      .setParameters({ questionId: questionId })
      .getMany();
    return responses;
  } catch (e) {
    throw new Error('Problem getting responses!');
  }
};

//Update a response
const updateResponse = async (responseId: number, newReponse: json) : Promise<?Response> => {
  try {
    const response = await db().findOneById(responseId);
    response.response = newReponse;
    await db().persist(response);
    return response;
  } catch(e) {
    throw new Error('Error updating response');
  }
}

export default {
  createResponse,
  getResponseById,
  getResponses,
  getResponsesByQuestionId,
  updateResponse
};
