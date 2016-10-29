package org.cuappdev.podcast.models;

/* Factory and entity for Episode. */

case class EpisodeFields (audiosearch_id: Long,
                          title: String,
                          description: String,
                          audio_url: String,
                          image_url: String,
                          series_id: Long) extends Fields

case class EpisodeEntity (dBInfo: DBInfo,
                          fields: EpisodeFields) extends Entity (dBInfo, fields)

object EpisodeFactory extends EntityFactory[EpisodeEntity, EpisodeFields] {

  def create (f: EpisodeFields) : EpisodeEntity = {
    new EpisodeEntity(DBInfoFactory.create(), f)
  }

  def update (e: EpisodeEntity, newFields: EpisodeFields) : EpisodeEntity = {
    new EpisodeEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}