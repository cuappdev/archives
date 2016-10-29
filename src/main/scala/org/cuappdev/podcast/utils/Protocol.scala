package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._
import java.sql.Timestamp

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json.{DeserializationException, JsNull, JsNumber, JsValue,
                   JsonFormat, RootJsonFormat, DefaultJsonProtocol, JsObject}

/*
* Formatting for each of the resources available .. as well as some
* implicit specifications and such
*/
trait Protocol extends DefaultJsonProtocol {

  // Amazing thread about this here: https://goo.gl/y79ggA
  implicit object TimestampFormat extends JsonFormat[Timestamp] {

    // Handle writing
    def write (obj: Timestamp) = JsNumber(obj.getTime)

    // Handle reading
    def read (json: JsValue) = json match {
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
