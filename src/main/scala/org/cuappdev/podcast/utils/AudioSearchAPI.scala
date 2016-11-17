package org.cuappdev.podcast.utils

/* Necessary for handling HTTP response */
import spray.json._
import DefaultJsonProtocol._

import scalaj.http._

/* Filled with AudioSearchAPI HTTP requests */
class AudioSearchAPI (audiosearchAppId: String, audiosearchSecret: String) {

  val signature = Base64.encodeString(audiosearchAppId + ":" + audiosearchSecret)
  val baseUrl = "https://www.audiosear.ch"
  val headers : Map[String, String] = Map("Authorization" -> ("Basic " + signature),
                    "Content-Type" -> "application/x-www-form-urlencoded")

  /* OAuth */
  val response = Http(baseUrl + "/oauth/token")
    .param("grant_type", "client_credentials")
    .headers(headers).postForm.asString.body

  /* Grab Access Token (.get b/c Option) */
  val accessToken = response.parseJson.asJsObject.fields.get("access_token").get

  /* Ensure we got it via print */
  println(accessToken)

}



/* Singleton */
object AudioSearch extends Config {
  val instance = new AudioSearchAPI (audiosearchAppId, audiosearchSecret)
}
