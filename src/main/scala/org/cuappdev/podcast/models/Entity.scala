package org.cuappdev.podcast.models

import java.sql.Timestamp
import org.joda.time.DateTime

abstract class Fields

class Entity (dBInfo: DBInfo, fields: Fields) {
  def getDBInfo : DBInfo = dBInfo
  def getFields : Fields = fields
}

abstract class EntityFactory [E <: Entity, F <: Fields] {
  def instantiate (dbInfo: DBInfo, newFields: F): E
  def create (f: F): E
  def update (e: E, newFields: F): E
}

case class DBInfo (id: Option[Long], created_at: Timestamp, updated_at: Timestamp)

object DBInfoFactory {
  def create (id: Option[Long] = None,
              created_at: Timestamp = new Timestamp(DateTime.now.getMillis),
              updated_at: Timestamp = new Timestamp(DateTime.now.getMillis)) : DBInfo = {
    new DBInfo(id, created_at, updated_at)
  }

  def update (e: DBInfo) : DBInfo = {
    new DBInfo(e.id, e.created_at, new Timestamp(DateTime.now.getMillis))
  }

}


