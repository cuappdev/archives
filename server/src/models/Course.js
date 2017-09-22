// @flow
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToMany,
  OneToMany,
  ManyToOne,
  JoinTable
} from 'typeorm';
import {Base} from './Base';
import {User} from './User';
import {Lecture} from './Lecture';
import {Organization} from './Organization';

@Entity('courses')
export class Course extends Base {
  @PrimaryGeneratedColumn()
  id: any = null;

  @Column('string')
  subject: string = '';

  @Column('number')
  catalogNum: number;

  @Column('string')
  name: string = '';

  @Column('string')
  term: string = '';

  @ManyToOne(type => Organization, organization => organization.courses)
  organization: Organization;

  @OneToMany(type => Lecture, lecture => lecture.course)
  lectures: Lecture[];

  @ManyToMany(type => User, user => user.adminCourses)
  admins: User[];

  @ManyToMany(type => User, user => user.enrolledCourses, {
    cascadeAll: true
  }) //Deals with if students add/drop course
  students: User[];
}
