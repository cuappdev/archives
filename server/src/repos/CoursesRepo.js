// @flow
import { getConnectionManager, Repository } from 'typeorm';
import {Course} from '../models/Course';
import {Organization} from '../models/Organization';
import OrganizationsRepo from './OrganizationsRepo';

const db = (): Repository<Course> => {
  return getConnectionManager().get().getRepository(Course);
};

// Create a course
const createCourse = async (subject: string, catalogNum: number, name: string,
  term: string, organizationId: number): Promise<Course> => {
  try {
    const course = new Course();
    course.subject = subject;
    course.catalogNum = catalogNum;
    course.name = name;
    course.term = term;
    course.organization = await OrganizationsRepo.getOrgById(organizationId);
    await db().persist(course);
    return course;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating course!');
  }
};

// Get a course by Id
const getCourseById = async (id: number): Promise<?Course> => {
  try {
    const course = await db().findOneById(id);
    return course;
  } catch (e) {
    throw new Error(`Problem getting course by id: ${id}!`);
  }
};

// Get courses
const getCourses = async (): Promise<Array<Course>> => {
  try {
    const courses = await db().createQueryBuilder('courses')
      .getMany();
    return courses;
  } catch (e) {
    throw new Error('Problem getting courses!');
  }
};

export default {
  createCourse,
  getCourseById,
  getCourses
};
