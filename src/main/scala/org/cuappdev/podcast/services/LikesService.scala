package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.LikeEntityTable
import org.cuappdev.podcast.models.{LikeEntity, LikeFields, LikeFactory}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

case class LikeNotFoundException(msg: String) extends Exception(msg: String)

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

  /**
    * Deletes a like.
    * @param id the ID of the like to delete
    * @return the ID of the deleted like
    */
  def deleteLike(id: Long) : Future[Option[Long]] = {
    val e : Future[Option[LikeEntity]] = getLikeByID(id)
    e.flatMap {
      case Some(entity) => {
        db.run(likes.filter(_.id === id).delete)
        Future.successful(Some(id)) }
      case None => Future.failed(new LikeNotFoundException("Like not found"))
    }
  }


}
