package org.cuappdev.podcast.models

import spray.json.{JsArray, JsNumber, JsString, JsValue}

/** Factory and entity for Series. **/

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

  def create (jsonVal : JsValue) : SeriesEntity = {
    val json = jsonVal.asJsObject
    val audiosearchID = json.fields("id").asInstanceOf[JsNumber].value.longValue()
    val title = json.fields("title").asInstanceOf[JsString].value
    val description = json.fields.get("description") match
      { case None => "" case Some(d) => d.asInstanceOf[JsString].value }
    val audioURL = json.fields("audio_files").asInstanceOf[JsArray]
      .elements.apply(0).asJsObject.fields("mp3").asInstanceOf[JsString].value
    val imageArr = json.fields("image_urls").asInstanceOf[JsArray]
    val imageURL =
      if (imageArr.elements.nonEmpty) imageArr.elements.apply(0)
        .asJsObject.fields("file").asJsObject.fields("url").asInstanceOf[JsString].value
      else  ""
    SeriesFactory.create(SeriesFields(audiosearchID, title, description, imageURL))
  }


  def update (e: SeriesEntity, newFields: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}