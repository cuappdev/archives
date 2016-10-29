package org.cuappdev.podcast.models

case class UserFields (fb_id: String) extends Fields

case class UserEntity (override val dBInfo: DBInfo,
                       override val fields: UserFields) extends Entity (dBInfo, fields)

object UserFactory extends EntityFactory[UserEntity, UserFields] {

  def create (f: UserFields) : UserEntity = {
    new UserEntity(DBInfoFactory.create(), f)
  }

  def update (e: UserEntity, newFields: UserFields) : UserEntity = {
    new UserEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}
