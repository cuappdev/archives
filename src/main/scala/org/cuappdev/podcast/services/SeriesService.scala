package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.SeriesEntityTable
import org.cuappdev.podcast.models.{SeriesEntity, SeriesFactory, SeriesFields}
import org.cuappdev.podcast.utils.{APIResponseDirectives, AudioSearch, Config, Protocol}
import spray.json._

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object SeriesService extends SeriesService

trait SeriesService extends SeriesEntityTable
  with APIResponseDirectives
  with Protocol {

  /** Search series via a query **/
  def searchSeries (query: String) : JsValue = {
    /* Grab API response */
    val series : JsArray = AudioSearch.getInstance.searchShows(query, Map())
                                          .asJsObject.fields("results").asInstanceOf[JsArray]
    /* Build result */
    val result = series.elements.map(j => SeriesFactory.create(j))
    /* JSON response */
    respond(success=true,
      data=JsObject("series" ->
        JsArray(result.map { s => s.toJson}.toVector)))
      .toJson
  }

  /** Get related series (given audiosearch id) **/
  def relatedSeries (id: String) : JsValue = {
    /* Get long value */
    val idLong = Integer.parseInt(id).toLong
    /* Grab API response */
    val series : JsArray = AudioSearch.getInstance.getShowRelated(idLong, Map()).asInstanceOf[JsArray]
    /* Build result */
    val result = series.elements.map(j => SeriesFactory.create(j))
    /* JSON response */
    respond(
      success=true,
      data=JsObject("series" ->
        JsArray(result.map {s => s.toJson}.toVector)))
      .toJson
  }

}
