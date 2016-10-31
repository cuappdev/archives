package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.EpisodeEntity
import org.cuappdev.podcast.utils.Config

import scala.concurrent.Future

object EpisodesService extends EpisodesService

trait EpisodesService extends EpisodeEntityTable with Config {

  import driver.api._

  // Get all the episodes
  def getEpisodes(): Future[Seq[EpisodeEntity]] = db.run(episodes.result)


  // Get an episode by ID
  def getByID(id: Long): Future[Option[EpisodeEntity]] = {
    db.run(episodes.filter(_.id == id).result.headOption)
  }


}







