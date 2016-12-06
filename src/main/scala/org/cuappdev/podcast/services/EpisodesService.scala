package org.cuappdev.podcast.services
import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeFactory}
import org.cuappdev.podcast.utils.{APIResponseDirectives, AudioSearch, Protocol}
import spray.json._

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable
  with APIResponseDirectives
  with Protocol {

  /** Search episodes via a query **/
  def searchEpisodes (query: String): JsValue = {
    /* Grab API response */
    val eps : JsArray = AudioSearch.getInstance.searchEpisodes(query, Map())
                                    .asJsObject.fields.get("results") match {
      case None => JsArray()
      case Some(JsNull) => JsArray()
      case Some(JsArray(d)) => JsArray(d)
      case _ => throw new Exception()
    }
    /* Build result */
    val result = eps.elements.map(j => EpisodeFactory.create(j))
    /* JSON response */
    respond(success=true,
      data=JsObject("episodes" ->
        JsArray(result.map { ep => ep.toJson }.toVector)))
      .toJson
  }

  /** Get related episodes (given audiosearch id) **/
  def relatedEpisodes (id: String) : JsValue = {
    /* Get long value */
    val idLong = Integer.parseInt(id).toLong
    /* Grab API response */
    val eps : JsArray = AudioSearch.getInstance.getEpisodeRelated(idLong, Map()).asInstanceOf[JsArray]
    /* Build result */
    val result = eps.elements.map(j => EpisodeFactory.create(j))
    /* JSON response */
    respond(
      success=true,
      data=JsObject("episodes" ->
        JsArray(result.map { ep => ep.toJson }.toVector)))
      .toJson
  }

}
