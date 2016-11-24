package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeEntity, EpisodeFactory, EpisodeFields}
import org.cuappdev.podcast.utils.{AudioSearch, Config}
import spray.json.{JsArray, JsNumber, JsObject, JsString, JsValue}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable with Config {
  import driver.api._

  /* Search episodes via a query */
  def searchEpisodes (query: String): Seq [EpisodeEntity] = {
    /* Grab API response */
    val eps : JsArray = AudioSearch.getInstance.searchEpisodes(query, Map())
                                    .asJsObject.fields("results").asInstanceOf[JsArray]
    /* Build result */
    eps.elements.map(jsonVal =>  EpisodeFactory.create(jsonVal))
  }

  /* Get related episodes (given audiosearch_id) */
  def relatedEpisodes (id: Long) : Seq [EpisodeEntity] = {
    /* Grab API response */
    val eps : JsArray = AudioSearch.getInstance.getEpisodeRelated(id, Map()).asInstanceOf[JsArray]
    /* Build result */
    eps.elements.map(jsonVal => EpisodeFactory.create(jsonVal))
  }

}
