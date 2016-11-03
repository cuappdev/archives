package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._
import java.sql.Timestamp

import com.sun.xml.internal.ws.encoding.soap.SerializationException

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json._


trait StockProtocol extends DefaultJsonProtocol {

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

  // EntityProtocol
  class EntityProtocol[F <: Fields, E <: Entity] (fieldFormat : RootJsonFormat[F],
                                                  factory: (DBInfo, F) => E) extends JsonFormat[E] {

    // DBInfo + Field subclass formatting
    implicit val dbInfoFormat = jsonFormat3(DBInfo)
    // JSON formatting for the fields
    implicit val thisFieldFormat = fieldFormat

    // Write entities
    def write (obj: E): JsValue = {
      (obj.getDBInfo.toJson, obj.getFields.asInstanceOf[F].toJson) match {
        case (JsObject(dbInfo), JsObject(fields)) => JsObject(dbInfo ++ fields)
        case _ => throw new SerializationException("This is entity is mal-formatted")
      }
    }

    // Reading entities
    def read (json: JsValue): E = {
      val dDbInfo = json.convertTo[DBInfo]
      val dFields = json.convertTo[F]
      factory(dDbInfo, dFields)
    }
  }


}
