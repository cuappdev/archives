package org.cuappdev.podcast.models

case class UserFields (fb_id: String) extends Fields

case class UserEntity (dBInfo: DBInfo,
                       fields: UserFields) extends Entity (dBInfo, fields)

object UserFactory extends EntityFactory[UserEntity, UserFields] {

  def instantiate(dbInfo: DBInfo, fields: UserFields) = {
    new UserEntity(dbInfo, fields)
  }

  def create (f: UserFields) : UserEntity = {
    new UserEntity(DBInfoFactory.create(), f)
  }

  def update (e: UserEntity, newFields: UserFields) : UserEntity = {
    new UserEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}
