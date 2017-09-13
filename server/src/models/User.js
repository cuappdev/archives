// @flow
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';
import {Base} from './Base';

@Entity('users')
export class User extends Base {
  @PrimaryGeneratedColumn()
  id: any = null; // hacky b/c https://github.com/babel/babel/issues/5519

  @Column('string')
  googleId: string = '';

  @Column('string')
  netId: string = '';

  @Column('string')
  firstName: string = '';

  @Column('string')
  lastName: string = '';

  @Column('string')
  email: string = '';

  static fromGoogleCreds (creds: Object): User {
    const u = new User();
    u.googleId = creds.googleId;
    u.netId = creds.netId;
    u.firstName = creds.firstName;
    u.lastName = creds.lastName;
    u.email = creds.email;
    return u;
  }
}
