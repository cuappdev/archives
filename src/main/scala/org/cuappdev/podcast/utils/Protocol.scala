package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._
import java.sql.Timestamp

import com.sun.xml.internal.ws.encoding.soap.SerializationException

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json._



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

  // DBInfo + Field subclass formatting
  implicit val dbInfoFormat = jsonFormat3(DBInfo)

  // EntityProtocol
  class EntityProtocol[F <: Fields, E <: Entity] (f: JsObject => F,
                                                  implicit val FieldFormat : RootJsonFormat[F],
                                                  factory: (DBInfo, F) => E) extends JsonFormat[E] {

    // Write entities
    def write (obj: E): JsValue = {
      (obj.getDBInfo.toJson, obj.getFields.asInstanceOf[F].toJson) match {
        case (dbInfo: JsObject, fields: JsObject) => a.copy(fields = fields ++ b.fields)
        case _ => throw new SerializationException("This is entity is malformatted")
      }
    }

    // Reading entities
    def read (json: JsValue): E = {
      json.asJsObject.getFields("id", "created_at", "updated_at") match {
        case Seq(JsNumber(id), JsNumber(created_at), JsNumber(updated_at)) =>
          // DB info, de-serialized
          val dDbInfo = DBInfo(Some(id.toLong),
            new Timestamp(created_at.toLong),
            new Timestamp(updated_at.toLong))
          // Fields, de-serialized
          val dFields = f(json.asJsObject)
          // Respond with an instance of Entity E
          factory(dDbInfo, dFields)
        case _ => throw new DeserializationException("Failed to read appropriate values")
      }
    }
  }


  // Episode formatting
  implicit val episodeFormat = new EntityProtocol[EpisodeFields, EpisodeEntity]((obj: JsObject) => {
    obj.getFields("audiosearch_id", "title", "description", "audio_url", "image_url", "series_id") match {
      case Seq(JsNumber(audiosearch_id),
               JsString(title),
               JsString(description),
               JsString(audio_url),
               JsString(image_url),
               JsNumber(series_id)) =>
                EpisodeFields(audiosearch_id.longValue,
                              title, description, audio_url, image_url, Some(series_id.longValue))
      case _ => throw new DeserializationException("Failed to deserialize episode")
    }
  }, jsonFormat6(EpisodeFields), EpisodeFactory.instantiate)


  // User formatting
  implicit val userFormat = new EntityProtocol[UserFields, UserEntity]((obj: JsObject) => {
    obj.getFields("fb_id") match {
      case Seq(JsString(fb_id)) => UserFields(fb_id)
      case _ => throw new DeserializationException("Failed to deserialize user")
    }
  }, jsonFormat1(UserFields), UserFactory.instantiate)




  // TODO: More models



}
