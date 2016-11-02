package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.LikeEntityTable
import org.cuappdev.podcast.models.LikeEntity
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future


object LikesService extends LikesService

trait LikesService extends LikeEntityTable with Config {

  import driver.api._

  // Get all the episodes
  def getLikes(): Future[Seq[LikeEntity]] = db.run(like.result)


  // Get an episode by ID
  def getByID(id: Long): Future[Option[LikeEntity]] = {
    db.run(like.filter(_.id === id).result.headOption)
  }


}