// @flow
import { getConnectionManager, Repository } from 'typeorm';
import {Course} from '../models/Course';
import {Organization} from '../models/Organization';
import {User} from '../models/User';
import OrganizationsRepo from './OrganizationsRepo';
import UsersRepo from './UsersRepo';

const db = (): Repository<Course> => {
  return getConnectionManager().get().getRepository(Course);
};

// Create a course
const createCourse = async (subject: string, catalogNum: number, name: string,
  term: string, organizationId: number, adminId: number): Promise<Course> => {
  try {
    const course = new Course();
    course.subject = subject;
    course.catalogNum = catalogNum;
    course.name = name;
    course.term = term;
    course.organization = await OrganizationsRepo.getOrgById(organizationId);

    const admin = await UsersRepo.getUserById(adminId);
    if(!admin) throw new Error('Problem getting admin from id!')
    course.admins = [admin];

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

// Get courses by org id
const getCoursesByOrgId = async (orgId: number): Promise<Array<Course>> => {
  try {
    const courses = await db().createQueryBuilder('courses')
      .innerJoinAndSelect("courses.organization", "organization")
      .where("organization.id=:orgId")
      .setParameters({ orgId: orgId })
      .getMany();
    return courses;
  } catch (e) {
    throw new Error('Problem getting courses!');
  }
};

// add students to course
const addStudents = async (courseId: number, studentIds: number[]): Promise<Course> => {
  try {
    const course = await db().findOneById(courseId);
    var students = course.students;
    for(var i = 0; i < studentIds.length; i++) {
      students.push(await UsersRepo.getUserById(studentIds[i]));
    }
    course.students = students;
    await db().persist(course);
    return course;
  } catch (e) {
    console.log(e);
    throw new Error('Problem adding students to course!');
  }
};

// add admins to course
const addAdmins = async (courseId: number, adminIds: number[]): Promise<Course> => {
  try {
    const course = await db().findOneById(courseId);
    var admins = course.admins;
    for(var i = 0; i < adminIds.length; i++) {
      admins.push(await UsersRepo.getUserById(adminIds[i]));
    }
    course.admins = admins;
    await db().persist(course);
    return course;
  } catch (e) {
    console.log(e);
    throw new Error('Problem adding admins to course!');
  }
};

// get students in course
const getStudents = async (courseId: number): Promise<Array<User>> => {
  try {
    const course = await db().createQueryBuilder('courses')
      .innerJoinAndSelect("courses.students", "students")
      .where("courses.id=:courseId")
      .setParameters({ courseId: courseId })
      .getOne();
    return course.students;
  } catch (e) {
    console.log(e);
    throw new Error('Problem getting students from course!');
  }
};

// get admins in course
const getAdmins = async (courseId: number): Promise<Array<User>> => {
  try {
    const course = await db().createQueryBuilder('courses')
      .innerJoinAndSelect("courses.admins", "admins")
      .where("courses.id=:courseId")
      .setParameters({ courseId: courseId })
      .getOne();
    return course.admins;
  } catch (e) {
    console.log(e);
    throw new Error('Problem getting admins from course!');
  }
};

export default {
  createCourse,
  getCourseById,
  getCourses,
  getCoursesByOrgId,
  addStudents,
  addAdmins,
  getStudents,
  getAdmins
};
