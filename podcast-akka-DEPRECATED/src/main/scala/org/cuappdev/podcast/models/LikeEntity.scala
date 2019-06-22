package org.cuappdev.podcast.models

/* Factory and entity for Like. */

case class LikeFields (user_id: Option[Long],
                       episode_id: Option[Long]) extends Fields

case class LikeEntity (dBInfo: DBInfo,
                       fields: LikeFields) extends Entity (dBInfo, fields)

object LikeFactory extends EntityFactory[LikeEntity, LikeFields] {

  def instantiate(dbInfo: DBInfo, newFields: LikeFields) = {
    new LikeEntity(dbInfo, newFields)
  }

  def create (f: LikeFields) : LikeEntity = {
    new LikeEntity(DBInfoFactory.create(), f)
  }

  def update (e: LikeEntity, newFields: LikeFields) : LikeEntity = {
    new LikeEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}