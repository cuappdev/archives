// @flow
import { getConnectionManager, Repository } from 'typeorm';
import {Lecture} from '../models/Lecture';
import {Course} from '../models/Course';
import CoursesRepo from './CoursesRepo';

const db = (): Repository<Lecture> => {
  return getConnectionManager().get().getRepository(Lecture);
};

// Create a lecture
const createLecture = async (datetime: number, courseId: number): Promise<Lecture> => {
  try {
    const lecture = new Lecture();
    lecture.dateTime = datetime;
    lecture.course = await CoursesRepo.getCourseById(courseId);
    await db().persist(lecture);
    return lecture;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating lecture!');
  }
};

// Get a lecture by Id
const getLectureById = async (id: number): Promise<?Lecture> => {
  try {
    const lecture = await db().findOneById(id);
    return lecture;
  } catch (e) {
    throw new Error(`Problem getting lecture by id: ${id}!`);
  }
};

// Get lectures
const getLectures = async (): Promise<Array<Lecture>> => {
  try {
    const lectures = await db().createQueryBuilder('lectures')
      .getMany();
    return lectures;
  } catch (e) {
    throw new Error('Problem getting lectures!');
  }
};

// Get lectures by course id
const getLecturesByCourseId = async (courseId: number): Promise<Array<Lecture>> => {
  try {
    const lectures = await db().createQueryBuilder('lectures')
      .innerJoin("lectures.course", "course", "course.id=:courseId")
      .setParameters({ courseId: courseId })
      .getMany();
    return lectures;
  } catch (e) {
    throw new Error('Problem getting lectures!');
  }
};

//Returns lectures in reverse chronological order starting at the cursor
//pageIndex must be > 0
const paginateLectureByCourseId = async(courseId: number, cursor: number, items: number,
  pageIndex: number): Promise<Array<Lecture>> => {
  try {
    const lectures = await db().createQueryBuilder('lectures')
      .innerJoin("lectures.course", "course", "course.id = :courseId")
      .where("lectures.createdAt <= :c")
      .setParameters( {courseId: courseId, c: cursor} )
      .orderBy("lectures.createdAt", "DESC")
      .setFirstResult((pageIndex-1) * items)
      .setMaxResults(items)
      .getMany();
    return lectures;
  } catch(e) {
    throw new Error('Problem getting lectures!');
  }
}

export default {
  createLecture,
  getLectureById,
  getLectures,
  getLecturesByCourseId,
  paginateLectureByCourseId
};
