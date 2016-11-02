package org.cuappdev.podcast.models

/* Factory and entity for Series. */

case class SeriesFields (audiosearch_id: Long,
                        title: String,
                        description: String,
                        imageUrl: String) extends Fields

case class SeriesEntity (dBInfo: DBInfo,
                         fields: SeriesFields) extends Entity (dBInfo, fields)

object SeriesFactory extends EntityFactory[SeriesEntity, SeriesFields] {

  def instantiate(dbInfo: DBInfo, newFields: SeriesFields) = {
    new SeriesEntity(dbInfo, newFields)
  }

  def create (f: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.create(), f)
  }

  def update (e: SeriesEntity, newFields: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}