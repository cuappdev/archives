package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.{UserFactory, UserFields}

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.EpisodeEntity
import org.cuappdev.podcast.utils.Config

// To deal with futures
import scala.util.{Success, Failure}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

trait EpisodesService extends EpisodeEntityTable with Config {

  import driver.api._

  // Gets all the episodes
  def getEpisodes(): Future[Seq[EpisodeEntity]] = db.run(episodes.result)


  // Get a user by fb_id
  def getByID(id: Long): Future[Option[EpisodeEntity]] = {
    db.run(episodes.filter(_.id == id).result.headOption)
  }


}







