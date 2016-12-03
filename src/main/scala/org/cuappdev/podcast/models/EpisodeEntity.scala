package org.cuappdev.podcast.models

import spray.json.{JsArray, JsNumber, JsString, JsValue}
;

/** Factory and entity for Episode. **/
case class EpisodeFields (audiosearch_id: Long,
                          title: String,
                          description: String,
                          audio_url: String,
                          image_url: String,
                          series_id: Option[Long]) extends Fields

case class EpisodeEntity (dBInfo: DBInfo,
                          fields: EpisodeFields) extends Entity (dBInfo, fields)

object EpisodeFactory extends EntityFactory[EpisodeEntity, EpisodeFields] {

  /** Necessary for JSON serialization **/
  def instantiate(dbInfo: DBInfo, newFields: EpisodeFields) = {
    new EpisodeEntity(dbInfo, newFields)
  }

  /** Creation from fields **/
  def create (f: EpisodeFields) : EpisodeEntity = {
    new EpisodeEntity(DBInfoFactory.create(), f)
  }

  /** From JSON from audiosear.ch **/
  def create (jsonVal: JsValue) : EpisodeEntity = {
    val json = jsonVal.asJsObject
    val audiosearchID = json.fields("id").asInstanceOf[JsNumber].value.longValue()
    val title = json.fields("title").asInstanceOf[JsString].value
    val description = json.fields.get("description") match
      { case None => "" case Some(d) => d.asInstanceOf[JsString].value }
    val audioArr = json.fields("audio_files").asInstanceOf[JsArray]
    val audioURL =
      if (audioArr.elements.nonEmpty)
        audioArr.elements.apply(0).asJsObject.fields("mp3").asInstanceOf[JsString].value
      else ""
    val imageURL = json.fields("image_urls").asJsObject.fields("full").asInstanceOf[JsString].value
    EpisodeFactory.create(EpisodeFields(audiosearchID, title, description, audioURL, imageURL, None))
  }

  /** Updates on diff-checking **/
  def update (e: EpisodeEntity, newFields: EpisodeFields) : EpisodeEntity = {
    new EpisodeEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}