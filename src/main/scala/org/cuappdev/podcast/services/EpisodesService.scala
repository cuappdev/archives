package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeEntity, EpisodeFactory, EpisodeFields}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable with Config {

  import driver.api._

  /** Gets all the episodes.
    * @return all of the episodes
    */
  def getEpisodes(): Future[Seq[EpisodeEntity]] = db.run(episodes.result)

  /**
    * Gets an episode with a specific ID.
    * @param id the ID of the episode
    * @return the episode entity
    */
  def getEpisodeByID(id: Long): Future[Option[EpisodeEntity]] = {
    db.run(episodes.filter(_.id === id).result.headOption)
  }

  /**
    * Deletes an episode.
    * @param id the ID of the episode to delete
    * @return the ID of the deleted episode
    */
  def deleteEpisode(id: Long) : Future[Option[Long]] = {
    val e : Future[Option[EpisodeEntity]] = getEpisodeByID(id)
    e.flatMap {
      case Some(entity) => {
        db.run(episodes.filter(_.id === id).delete)
        Future.successful(Some(id)) }
      case None => Future.failed(new EpisodeNotFoundException("Episode not found"))
    }
  }


}
