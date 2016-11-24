package org.cuappdev.podcast.utils

/* Necessary for handling HTTP response */
import java.net.URLEncoder
import spray.json._
import DefaultJsonProtocol._
import scalaj.http._


/* AudioSearchAPI HTTP requests */
class AudioSearchAPI (audiosearchAppId: String, audiosearchSecret: String) {

  val logStuff = false

  /* Fields */
  val baseUrl : String = "https://www.audiosear.ch"
  var accessToken: String = getAccessToken

  /* Gets an access token */
  def getAccessToken: String = {
    val signature = Base64.encodeString(audiosearchAppId + ":" + audiosearchSecret)
    val headers : Map[String, String] = Map("Authorization" -> ("Basic " + signature),
      "Content-Type" -> "application/x-www-form-urlencoded")
    Http(baseUrl + "/oauth/token")
      .param("grant_type", "client_credentials")
      .headers(headers).postForm.asString.body.parseJson.asJsObject.fields("access_token").asInstanceOf[JsString].value
  }

  /* Perform a GET request */
  def performGet (url: String, params: Map [String, String]) : JsValue = {
    val headers : Map[String, String] =
      Map("Authorization" -> ("Bearer " + accessToken))
    Http(baseUrl + "/api" + url).params(params).headers(headers).asString.body.parseJson
  }

  /* Log */
  def log (j: JsValue) {
    if (logStuff) {
      println("********* RESULTANT JSVALUE *********")
      println(j.toString)
    }
  }

  /* GET wrapper for audiosearch (auto-refreshes on command) */
  def get (url: String, params: Map[String, String]): JsValue = {
    var result = performGet(url, params)
    try {
      if (result.asJsObject.fields("status").asInstanceOf[JsString].value.equals("failure")) {
        accessToken = getAccessToken
        result = performGet(url, params)
        log(result)
        result
      } else {
        log(result)
        result
      }
    } catch {
      case e : Exception => {
        log(result)
        result
      }
    }
  }

  /* String -> URI UTF-8 encoding helper */
  def encodeURI (v: String) : String = {
    URLEncoder.encode(v, "utf-8")
  }

  /* Get episode by ID assigned by audiosearch */
  def getEpisode (id: Integer, params: Map [String, String]) : JsValue = {
    get ("/episodes/" + id.toString, params)
  }

  /* Get episodes that are related to a specific episode */
  def getEpisodeRelated (id: Integer, params: Map [String, String]) : JsValue = {
    get ("/episodes/" + id.toString + "/related", params)
  }

  /* Search episodes */
  def searchEpisodes (queryString: String, params: Map [String, String]) : JsValue = {
    get ("/search/episodes/" + encodeURI(queryString), params)
  }

  /* Get show by ID assigned by audiosearch */
  def getShow (id: Integer, params: Map [String, String]) : JsValue = {
    get ("/shows/" + id.toString, params)
  }

  /* Get shows that are related to a specific show */
  def getShowRelated (id: Integer, params: Map [String, String]) : JsValue = {
    get ("/shows/" + id.toString + "/related", params)
  }

  /* Get statistics of a specific show */
  def getShowStats (id: Integer, params: Map [String, String]) : JsValue = {
    get ("/shows/" + id.toString + "/stats", params)
  }

  /* Search shows */
  def searchShows (queryString: String, params: Map [String, String]) : JsValue = {
    get ("/search/shows/" + encodeURI(queryString), params)
  }

}


/* Singleton */
object AudioSearch extends Config {
  var instance : Option[AudioSearchAPI] = None
  val getInstance : AudioSearchAPI = {
    instance match {
      case None    => new AudioSearchAPI(audiosearchAppId, audiosearchSecret)
      case Some(i) => i
    }
  }
}


