package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeEntity, EpisodeFactory, EpisodeFields}
import org.cuappdev.podcast.utils.Config

import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable with Config {

  import driver.api._

  /**
    * Creates a new episode given some fields.
    * @param fields the EpisodeFields needed to create the EpisodeEntity
    * @return the newly created EpisodeEntity
    */
  def createEpisode(fields : EpisodeFields): Future[Option[EpisodeEntity]] = {
    val newEpisode = EpisodeFactory.create(fields)
    db.run(episodes returning episodes += newEpisode)
    Future.successful(Some(newEpisode))
  }

  /** Gets all the episodes.
    * @return all of the episodes
    */
  def getEpisodes(): Future[Seq[EpisodeEntity]] = db.run(episodes.result)

  /**
    * Gets an episode with a specific ID.
    * @param id the ID of the episode
    * @return the episode entity
    */
  def getByID(id: Long): Future[Option[EpisodeEntity]] = {
    db.run(episodes.filter(_.id == id).result.headOption)
  }

  /**
    * Updates an episode.
    * @param id the ID of the episode
    * @param fields the EpisodeFields containing new values
    * @return an EpisodeEntity updated with the new fields
    */
  def updateEpisode(id: Long, fields: EpisodeFields): Future[Option[EpisodeEntity]] = {
    val e : Future[Option[EpisodeEntity]] = getByID(id)
    e.flatMap {
      case Some(entity) => Future.successful(Some(EpisodeFactory.update(entity, fields)))
      case None => Future.failed(new EpisodeNotFoundException("Episode not found"))
    }
  }

  /**
    * Deletes an episode.
    * @param id the ID of the episode to delete
    * @return the ID of the deleted episode
    */
  def deleteEpisode(id: Long) : Future[Option[Long]] = {
    val e : Future[Option[EpisodeEntity]] = getByID(id)
    e.flatMap {
      case Some(entity) => /* TODO: delete here */ Future.successful(Some(id))
      case None => Future.failed(new EpisodeNotFoundException("Episode not found"))
    }
  }


}







