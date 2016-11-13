package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.LikeEntityTable
import org.cuappdev.podcast.models.{LikeEntity, LikeFields, LikeFactory}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future


object LikesService extends LikesService

trait LikesService extends LikeEntityTable with Config {

  import driver.api._

  /**
    * Creates a new like given some fields.
    * @param fields the LikeFields needed to create the LikeEntity
    * @return the newly created LikeEntity
    */
  def createLike(fields : LikeFields): Future[Option[LikeEntity]] = {
    val newLike = LikeFactory.create(fields)
    db.run(likes returning likes += newLike)
    Future.successful(Some(newLike))
  }

  // Get all the episodes
  def getLikes(): Future[Seq[LikeEntity]] = db.run(likes.result)


  // Get an episode by ID
  def getLikeByID(id: Long): Future[Option[LikeEntity]] = {
    db.run(likes.filter(_.id === id).result.headOption)
  }


}
