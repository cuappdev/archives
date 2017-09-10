// @flow
import { Entity, PrimaryColumn, Column } from 'typeorm';
import {Base} from './Base';

@Entity('users')
export class User extends Base {
  @PrimaryColumn('int', { generated: true })
  id: ?number = null;

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
