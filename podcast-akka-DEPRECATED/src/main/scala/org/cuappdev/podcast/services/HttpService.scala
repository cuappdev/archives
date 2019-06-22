package org.cuappdev.podcast.services

import org.cuappdev.podcast.utils.{APIResponseDirectives, Protocol}
import spray.json._

/* Execution requirements */
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object HttpService extends HttpService

trait HttpService extends EpisodesService with SeriesService
  with APIResponseDirectives
  with Protocol {

  /** Get all search results **/
  def searchEverything (query : String) : JsValue = {

    /* Both search results */
    val searchEp = searchEpisodes(query).asJsObject.fields("data").asJsObject.fields("episodes")
    val searchSe = searchSeries(query).asJsObject.fields("data").asJsObject.fields("series")

    /* JSON response */
    respond(success=true,
      data=JsObject("episodes" -> searchEp, "series" -> searchSe)).toJson
  }

}
