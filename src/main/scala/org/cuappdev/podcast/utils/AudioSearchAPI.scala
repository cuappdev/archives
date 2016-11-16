package org.cuappdev.podcast.utils

import akka.http.scaladsl.model.HttpResponse
import scalaj.http._

/* Filled with AudioSearchAPI HTTP requests */
class AudioSearchAPI (audiosearchAppId: String, audiosearchSecret: String) {

  val baseUrl = "https://www.audiosear.ch"
  val headers : Map[String, String] = Map("Authorization" -> ("Basic " + audiosearchAppId + ":" + audiosearchSecret),
                    "Content-Type" -> "application/x-www-form-urlencoded")

  val oAuthResponse = Http(baseUrl + "/oauth/token").param("grant_type", "client_credentials").headers(headers)
}



/* Singleton */
object AudioSearch extends Config {
  val instance = new AudioSearchAPI (audiosearchAppId, audiosearchSecret)
}
