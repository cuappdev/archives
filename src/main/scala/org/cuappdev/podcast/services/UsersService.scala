package org.cuappdev.podcast.services

// Facebook
import com.restfb.DefaultFacebookClient
import com.restfb.FacebookClient
import com.restfb.Version

// User entity + db stuff
import me.archdev.restapi.models.db.UserEntityTable
import me.archdev.restapi.models.UserEntity

// To deal with futures
import scala.util.{Success, Failure}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object UsersService extends UsersService

trait UsersService extends UserEntityTable with Config {

  import driver.api._

  // Gets all the users
  def getUsers(): Future[Seq[UserEntity]] = db.run(users.result)


  // Get a user by fb_id
  def getByFbID(fb_id: String): Future[Option[UserEntity]] = {
    db.run(users.filter(_.fb_id === fb_id).result.headOption)
  }


  // Gets a user via FB authentication
  def getOrCreateUser(fb_token: String): Future[Option[UserEntity]] = {
    // Grab fb info
    val fb: FacebookClient = new DefaultFacebookClient(fb_token, facebookSecret, Version.VERSION_2_8)
    val fb_user: com.restfb.types.User = fb.fetchObject("me", classOf[com.restfb.types.User])

    // See if the user exists
    val u: Future[Option[UserEntity]] = this.getByFbID(fb_user.getId)
    u.flatMap {
      // If we have this user already
      case Some(user) => Future.successful(Some(user))
      // If we don't have this user already
      case None => {
        val newUser = UserEntity(fb_user.getId)
        db.run(users returning users += newUser)
        Future.successful(Some(newUser))
      }
    }
  }


}







