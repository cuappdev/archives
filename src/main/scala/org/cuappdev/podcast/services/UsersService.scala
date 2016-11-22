package org.cuappdev.podcast.services

// Facebook
import com.restfb.DefaultFacebookClient
import com.restfb.FacebookClient
import com.restfb.Version
import org.cuappdev.podcast.models.{UserFactory, UserFields, SessionEntity, SessionFields, SessionFactory}
import org.cuappdev.podcast.services.SessionsService

// User entity + db stuff
import org.cuappdev.podcast.models.db.{UserEntityTable, SessionEntityTable}
import org.cuappdev.podcast.models.UserEntity
import org.cuappdev.podcast.utils.Config

// To deal with futures
import scala.util.{Success, Failure}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object UsersService extends UsersService

case class UserNotFoundException(msg: String) extends Exception(msg: String)

trait UsersService extends UserEntityTable with SessionEntityTable with Config {

  import driver.api._

  /**
    * Gets all the users
    * @return - Future
    */
  def getUsers(): Future[Seq[UserEntity]] = db.run(users.result)


  /**
    * Get a user by Facebook ID
    * @param fb_id - String
    * @return - Future
    */
  def getUserByFbID(fb_id: String): Future[Option[UserEntity]] = {
    db.run(users.filter(_.fb_id === fb_id).result.headOption)
  }

  /**
    * Get a user by ID
    * @param id - The ID of the user to get (Long)
    * @return - Future
    */
  def getUserByID(id: Long): Future[Option[UserEntity]] = {
    db.run(users.filter(_.id === id).result.headOption)
  }

  /**
    * Gets a user via FB authentication
    * @param fb_token - The FB Token characterizing the user (String)
    * @return - Future with the UserEntity
    */
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
        getOrCreateUserSession(newUser)
        Future.successful(Some(newUser))
      }
    }
  }

  def getOrCreateUserSession(user: UserEntity) : Future[Option[SessionEntity]] = {
    val session : Future[Option[SessionEntity]] = db.run(sessions.filter(_.user_id === user.dBInfo.id).result.headOption)
    session.flatMap {
      case Some(s) => Future.successful(Some(s))
      case None => val s = SessionFactory.create(
        new SessionFields(
          SessionsService.generateToken(),
          SessionsService.generateToken(),
          SessionsService.generateExpiresAt(),
          user.dBInfo.id)
        );
        Future.successful(Some(s))
    }
  }

  /**
    * Deletes a user
    * @param id - The ID of the user to delete (Long)
    * @return - Future with the ID of the deleted subscription
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
