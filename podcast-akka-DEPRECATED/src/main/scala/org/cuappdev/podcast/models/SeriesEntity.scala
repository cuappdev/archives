package org.cuappdev.podcast.models

import spray.json._

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
    val title = json.fields.get("title") match {
      case None => ""
      case Some(JsString(d)) => d
      case Some(JsNull) => ""
    }
    val description = json.fields.get("description") match {
      case None => ""
      case Some(JsString(d)) => d
      case Some(JsNull) => ""
    }
    val imageArr = json.fields.get("image_files") match {
      case None => JsArray()
      case Some(JsArray(d)) => JsArray(d)
      case Some(JsNull) => JsArray()
    }
    val imageURL =
      if (imageArr.elements.nonEmpty)
        imageArr.elements.apply(0).asJsObject.fields("file").asJsObject.fields.get("url") match {
          case None => ""
          case Some(JsString(d)) => d
          case Some(JsNull) => ""
        }
      else  ""
    SeriesFactory.create(SeriesFields(audiosearchID, title, description, imageURL))
  }


  def update (e: SeriesEntity, newFields: SeriesFields) : SeriesEntity = {
    new SeriesEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}