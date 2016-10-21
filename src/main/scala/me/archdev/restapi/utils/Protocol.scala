package me.archdev.restapi.utils

import me.archdev.restapi.models._

// Incredibly useful JSON implementation in Scala
// https://github.com/spray/spray-json
import spray.json.DefaultJsonProtocol


/* Formatting for each of the resources available */
trait Protocol extends DefaultJsonProtocol {

  // TODO: modify these to be actual models
  implicit val usersFormat = jsonFormat3(UserEntity)
  implicit val tokenFormat = jsonFormat3(TokenEntity)


}
