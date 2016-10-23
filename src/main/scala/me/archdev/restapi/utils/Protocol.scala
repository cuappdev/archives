package me.archdev.restapi.utils

import me.archdev.restapi.models._
import spray.json.{DeserializationException, JsNull, JsNumber, JsValue, JsonFormat}
import java.sql.Timestamp

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json.DefaultJsonProtocol


/*
* Formatting for each of the resources available .. as well as some
* implicit specifications and such
*/
trait Protocol extends DefaultJsonProtocol {

  // Amazing thread about this here: https://goo.gl/y79ggA
  implicit object TimestampFormat extends JsonFormat[Option[Timestamp]] {

    // Handle writing
    def write (obj: Option[Timestamp]) = obj match {
      case Some(ts) => JsNumber(ts.getTime)
      case None => JsNull
    }

    // Handle reading
    def read (json: JsValue) = json match {
      case JsNumber(time) => Some(new Timestamp(time.toLong))
      case JsNull => None
    }

  }


  // JSON formatting for each type of entity
  implicit val usersFormat = jsonFormat4(UserEntity)


}
