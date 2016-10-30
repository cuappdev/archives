package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._
import java.sql.Timestamp

import com.sun.xml.internal.ws.encoding.soap.SerializationException

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json._


/**
  *
  * @tparam F
  * @tparam E
  */
class EntityProtocol[F <: Fields, E <: Entity] extends JsonFormat[E] with DefaultJsonProtocol {

  // DB info format
  implicit val dbInfoFormat = jsonFormat3(DBInfo)

  // Grab the field format of whatever fields we're serializing
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
    val entityFields = value.asJsObject.fields
    

  }

}


/*
* Formatting for each of the resources available .. as well as some
* implicit specifications and such
*/
trait Protocol extends DefaultJsonProtocol {

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

  // Stock json info
  implicit val dbInfoFormat = jsonFormat3(DBInfo)

  // JSON formatting for each type of entity
  implicit val usersFieldsFormat = jsonFormat1(UserFields)
  implicit val usersFormat = jsonFormat2(UserEntity)
  // TODO: Write a function that generically handles generating a format for entities like 'users'


}
