package org.cuappdev.podcast.models

import java.sql.Timestamp

/* Factory and entity for Session. */

case class SessionFields (token: String,
                          update_token: String,
                          expires_at: Timestamp,
                          user_id: Option[Long]) extends Fields

case class SessionEntity (dBInfo: DBInfo,
                         fields: SessionFields) extends Entity (dBInfo, fields)

object SessionFactory extends EntityFactory[SessionEntity, SessionFields] {

  def instantiate(dbInfo: DBInfo, newFields: SessionFields) = {
    new SessionEntity(dbInfo, newFields)
  }

  def create (f: SessionFields) : SessionEntity = {
    new SessionEntity(DBInfoFactory.create(), f)
  }

  def update (e: SessionEntity, newFields: SessionFields) : SessionEntity = {
    new SessionEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}
