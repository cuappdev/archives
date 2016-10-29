package me.archdev.restapi.models

import java.sql.Timestamp
import org.joda.time.DateTime

abstract class Fields

abstract case class Entity (dBInfo: DBInfo, fields: Fields)

abstract class EntityFactory [E <: Entity, F <: Fields] {
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


