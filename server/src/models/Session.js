// @flow
import { Entity, PrimaryColumn, Column, OneToOne, JoinColumn } from 'typeorm';
import {Base} from './Base';
import {User} from './User';

@Entity('sessions')
export class Session extends Base {
  @PrimaryColumn('int', { generated: true })
  id: number;

  @Column('string')
  sessionToken: string = '';

  @Column('bigint')
  expiresAt: number = -1;

  @Column('string')
  updateToken: string = '';

  @Column('boolean')
  isActive: boolean = true;

  @OneToOne(type => User)
  @JoinColumn()
  userId: number = -1;
}
