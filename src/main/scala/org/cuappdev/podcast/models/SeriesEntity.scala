package org.cuappdev.podcast.models

/* Factory and entity for Series. */

case class SeriesFields (
                          /* define fields here */
                        ) extends Fields

case class SeriesEntity (dBInfo: DBInfo,
                         fields: SeriesFields) extends Entity (dBInfo, fields)

object SeriesFactory extends EntityFactory[SeriesEntity, SeriesFields] {

  def create (f: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.create(), f)
  }

  def update (e: SeriesEntity, newFields: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}