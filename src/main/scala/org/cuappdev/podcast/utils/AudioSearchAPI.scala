package org.cuappdev.podcast.utils

/* Necessary for handling HTTP response */
import java.net.URLEncoder
import spray.json._
import DefaultJsonProtocol._
import scalaj.http._


/* Filled with AudioSearchAPI HTTP requests */
class AudioSearchAPI (audiosearchAppId: String, audiosearchSecret: String) {

  /* Required fields */
  val baseUrl : String = "https://www.audiosear.ch"
  var accessToken : String = getAccessToken ()


  /* To get a new access token */
  def getAccessToken (): String = {
    val signature = Base64.encodeString(audiosearchAppId + ":" + audiosearchSecret)
    val headers : Map[String, String] = Map("Authorization" -> ("Basic " + signature),
      "Content-Type" -> "application/x-www-form-urlencoded")
    Http(baseUrl + "/oauth/token")
      .param("grant_type", "client_credentials")
      .headers(headers).postForm.asString.body.parseJson.asJsObject.fields.get("access_token").get.toString
  }

  /* GET wrapper for audiosearch */
  def get (url: String, params: Map[String, String]): JsObject = {
    val headers : Map[String, String] = Map("Authorization" -> ("Bearer " + accessToken),
      "User-Agent" -> "request")
    Http(url).params(params).headers(headers).asString.body.parseJson.asJsObject
  }

  /* String -> URI UTF-8 encoding helper */
  def encodeURI (v: String) : String = {
    URLEncoder.encode(v, "utf-8")
  }

  /* Get episode by ID assigned by audiosearch */
  def getEpisode (id: Integer, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/episodes/" + id.toString, params)
  }

  /* Get episodes that are related to a specific episode */
  def getEpisodeRelated (id: Integer, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/episodes/" + id.toString + "/related", params)
  }

  /* Search episodes */
  def searchEpisodes (queryString: String, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/search/episodes/" + encodeURI(queryString), params)
  }

  /* Get trending episodes */
  def trendingEpsiodes (params: Map [String, String]) : JsObject = {
    get (baseUrl + "/trending/", params)
  }

  /* Get show by ID assigned by audiosearch */
  def getShow (id: Integer, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/shows/" + id.toString, params)
  }

  /* Get shows that are related to a specific show */
  def getShowRelated (id: Integer, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/shows/" + id.toString + "/related", params)
  }

  /* Get statistics of a specific show */
  def getShowStats (id: Integer, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/shows/" + id.toString + "/stats", params)
  }

  /* Search shows */
  def searchShows (queryString: String, params: Map [String, String]) : JsObject = {
    get (baseUrl + "/search/shows/" + encodeURI(queryString), params)
  }

}


/* Singleton */
object AudioSearch extends Config {
  val instance = new AudioSearchAPI (audiosearchAppId, audiosearchSecret)
}
