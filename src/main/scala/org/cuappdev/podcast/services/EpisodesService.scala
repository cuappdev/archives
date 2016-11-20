package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeEntity, EpisodeFactory, EpisodeFields}
import org.cuappdev.podcast.utils.{AudioSearch, Config}
import spray.json.JsObject

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable with Config {

  import driver.api._

  /**
    * TODO
    * @return
    */
  def getEpisodes(): JsObject = AudioSearch.instance.trendingEpsiodes(Map())

  /**
    * Gets an episode with a specific ID.
    * @param id the ID of the episode
    * @return the episode entity
    */
  def getEpisodeByID(id: Long): Future[Option[EpisodeEntity]] = {
    db.run(episodes.filter(_.id === id).result.headOption)
  }



}
