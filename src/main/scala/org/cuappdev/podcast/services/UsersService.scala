package org.cuappdev.podcast.services

// Facebook
import com.restfb.DefaultFacebookClient
import com.restfb.FacebookClient
import com.restfb.Version
import org.cuappdev.podcast.models.{UserFactory, UserFields}

// User entity + db stuff
import org.cuappdev.podcast.models.db.UserEntityTable
import org.cuappdev.podcast.models.UserEntity
import org.cuappdev.podcast.utils.Config

// To deal with futures
import scala.util.{Success, Failure}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object UsersService extends UsersService

case class UserNotFoundException(msg: String) extends Exception(msg: String)

trait UsersService extends UserEntityTable with Config {

  import driver.api._

  // Gets all the users
  def getUsers(): Future[Seq[UserEntity]] = db.run(users.result)


  // Get a user by fb_id
  def getUserByFbID(fb_id: String): Future[Option[UserEntity]] = {
    db.run(users.filter(_.fb_id === fb_id).result.headOption)
  }

  // Get a user by ID
  def getUserByID(id: Long): Future[Option[UserEntity]] = {
    db.run(users.filter(_.id === id).result.headOption)
  }


  // Gets a user via FB authentication
  def getOrCreateUser(fb_token: String): Future[Option[UserEntity]] = {
    // Grab fb info
    val fb: FacebookClient = new DefaultFacebookClient(fb_token, facebookSecret, Version.VERSION_2_8)
    val fb_user: com.restfb.types.User = fb.fetchObject("me", classOf[com.restfb.types.User])

    // See if the user exists
    val u: Future[Option[UserEntity]] = this.getUserByFbID(fb_user.getId)
    u.flatMap {
      // If we have this user already
      case Some(user) => Future.successful(Some(user))
      // If we don't have this user already
      case None => {
        val newUser = UserFactory.create(UserFields(fb_user.getId))
        db.run(users returning users += newUser)
        Future.successful(Some(newUser))
      }
    }
  }

  /**
    * Deletes a user.
    * @param id the ID of the subscription to delete
    * @return the ID of the deleted subscription
    */
  def deleteUser(id: Long) : Future[Option[Long]] = {
    val e : Future[Option[UserEntity]] = getUserByID(id)
    e.flatMap {
      case Some(entity) => {
        db.run(users.filter(_.id === id).delete)
        Future.successful(Some(id)) }
      case None => Future.failed(new UserNotFoundException("Like not found"))
    }
  }

}
