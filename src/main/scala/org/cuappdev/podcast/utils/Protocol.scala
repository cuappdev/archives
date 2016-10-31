package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._
import java.sql.Timestamp

import com.sun.xml.internal.ws.encoding.soap.SerializationException

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json._

class EntityProtocol[F <: Fields, E <: Entity] (f: JsObject => F)
          extends JsonFormat[E] with DefaultJsonProtocol {

  // Amazing thread about this here: https://goo.gl/y79ggA
  implicit object TimestampFormat extends JsonFormat[Timestamp] {

    // Handle writing
    def write(obj: Timestamp) = JsNumber(obj.getTime)

    // Handle reading
    def read(json: JsValue) = json match {
      case JsNumber(time) => new Timestamp(time.toLong)
      case _ => throw DeserializationException("Should be a number")
    }

  }

  // DBInfo + Field subclass formatting
  implicit val dbInfoFormat = jsonFormat3(DBInfo)
  implicit val fieldFormat = jsonFormat1(Class[F])

  // What WOULD be the formatter for an entity
  implicit val entityFormat = jsonFormat2(Class[E])

  // Write entities
  def write (e : E) {
    (e.getDBInfo.toJson, e.getFields.toJson) match {
      case (JsObject(dbInfo), JsObject(fields)) => dbInfo ++ fields
      case _ => throw new SerializationException("This is entity is malformatted")
    }
  }

  // Reading entities
  def read (value: JsValue) {
    value.asJsObject.getFields("id", "created_at", "updated_at") match {
      case Seq(JsNumber(id), JsNumber(created_at), JsNumber(updated_at)) =>
        // DB info, de-serialized
        val dDbInfo = DBInfo(Some(id.toLong),
          new Timestamp(created_at.toLong),
          new Timestamp(updated_at.toLong))
        // Fields, de-serialized
        val dFields = f(value.asJsObject)
        new E(dDbInfo, dFields)
      case _ => throw new DeserializationException("Failed to read appropriate values")
    }
  }
}

trait Protocol extends DefaultJsonProtocol {

  // Stock json info
  implicit val dbInfoFormat = jsonFormat3(DBInfo)

  // User formatting
  implicit val userFormat = new EntityProtocol[UserFields, UserEntity]((obj: JsObject) => {
    obj.getFields("fb_id") match {
      case Seq(JsString(fb_id)) => UserFields(fb_id)
      case _ => throw new DeserializationException("Failed to deserialize user")
    }
  })

  // Other model formatting


}
