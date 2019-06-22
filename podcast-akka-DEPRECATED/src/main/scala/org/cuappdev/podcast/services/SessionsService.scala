package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.{SessionEntityTable, UserEntityTable}
import org.cuappdev.podcast.models.{SessionEntity, SessionFields, SessionFactory, UserEntity}
import org.cuappdev.podcast.utils.Config

import java.sql.Timestamp
import java.util.UUID
import org.joda.time.DateTime

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object SessionsService extends SessionsService

case class SessionNotFoundException(msg: String) extends Exception(msg: String)
case class SessionExpiredException(msg: String) extends Exception(msg: String)

trait SessionsService extends SessionEntityTable with UserEntityTable with Config {

  import driver.api._

  /** Helper function for generating a session token. **/
  def generateToken() : String = UUID.randomUUID().toString


  /** Helper function that creates an 'expires_at' time for a session. **/
  def generateExpiresAt() : Timestamp = {
    val ttl : Long = 300000
    new Timestamp(DateTime.now.getMillis + ttl)
  }

  /** Checks if the session is valid (i.e. not expired) **/
  def sessionValid(session: SessionEntity) : Boolean = {
    session.fields.expires_at.getTime > DateTime.now.getMillis
  }

  /** Grabs a user by the session's token (as long as the session is not expired) **/
  def grabUserBySessionToken(token: String) : Future[UserEntity] = {
    val session : Future[Option[SessionEntity]] =
      db.run(sessions.filter(_.token === token).result.headOption)

    /* Pull the session from the Future */
    session.flatMap {
      /* If the session exists */
      case Some(s) =>
        if (sessionValid(s)) {
          val user : Future[Option[UserEntity]] =
            db.run(users.filter(_.id === s.fields.user_id).result.headOption);
          user.flatMap {
            case Some(u) => Future.successful(u)
            case None => Future.failed(UserNotFoundException("User not found."))
          }
        } else {
          Future.failed(SessionExpiredException("This session has expired."))
        }
      /* If the session doesn't exist */
      case None =>
        Future.failed(SessionNotFoundException("Session not found by that token."))
    }
  }

  /** Creates a session after FB Authentication on a user **/
  def sessionFromUser(user: UserEntity) : Future[SessionEntity] = {
    val session : Future[Option[SessionEntity]] =
      db.run(sessions.filter(_.user_id === user.dBInfo.id).result.headOption)
    session.flatMap {
      case Some(s) =>
        val updatedSession = SessionFactory.update(s,
          SessionFields(generateToken(),
            generateToken(),
            generateExpiresAt(),
            s.fields.user_id))
        db.run(sessions.filter(_.id === s.dBInfo.id)
          .update(updatedSession)).map(_ => updatedSession)
      case None =>
        val newSession = SessionFactory.create(
          SessionFields(
            SessionsService.generateToken(),
            SessionsService.generateToken(),
            SessionsService.generateExpiresAt(),
            user.dBInfo.id)
        )
        db.run(sessions returning sessions += newSession)
    }
  }

  /** Updates a session and responds given an updateToken **/
  def updateSession(updateToken: String) : Future[Option[SessionEntity]] = {
    /* Grab old session via an update token */
    val session : Future[Option[SessionEntity]] =
      db.run(sessions.filter(_.update_token === updateToken).result.headOption)

    /* Pull the session from the Future */
    session.flatMap {
      /* If the session exists */
      case Some(s) =>
        /* Update the session */
        val session = SessionFactory.update(s,
          SessionFields(generateToken(),
                        generateToken(),
                        generateExpiresAt(),
                        s.fields.user_id))
        /* Update the session & return it in a Future */
        db.run(sessions.filter(_.id === s.dBInfo.id).update(session)).map(_ => Some(session))
      /* If the session does not exist */
      case None =>
        Future.failed(SessionNotFoundException("Session not found by that update token."))
    }
  }


}
