package org.cuappdev.podcast.models

/* Factory and entity for Like. */

case class LikeFields (
                        /* define fields here */
                      ) extends Fields

case class LikeEntity (override val dBInfo: DBInfo,
                       override val fields: LikeFields) extends Entity (dBInfo, fields)

object LikeFactory extends EntityFactory[LikeEntity, LikeFields] {

  def create (f: LikeFields) : LikeEntity = {
    new LikeEntity(DBInfoFactory.create(), f)
  }

  def update (e: LikeEntity, newFields: LikeFields) : LikeEntity = {
    new LikeEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}