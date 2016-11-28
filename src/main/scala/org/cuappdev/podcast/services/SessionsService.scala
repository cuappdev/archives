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
  def generateToken() : String = {
    UUID.randomUUID().toString()
  }

  /** Helper function that creates an 'expires_at' time for a session. **/
  def generateExpiresAt() : Timestamp = {
    val ttl : Long = 300000;
    new Timestamp(DateTime.now.getMillis + ttl)
  }

  /** Checks if the session is valid (i.e. not expired) **/
  def checkSessionValid(session: Future[Option[SessionEntity]]) : Future[Boolean] = {
    session.flatMap {
      case Some(s) => Future.successful(s.fields.expires_at.getTime > DateTime.now.getMillis)
      case None => {
        Future.failed(new SessionNotFoundException("Session not found"))
      }
    }
  }

  /** Grabs a user by the session's token (as long as the session is not expired) **/
  def grabUserBySessionToken(token: String) : Future[UserEntity] = {
    val session : Future[Option[SessionEntity]] = db.run(sessions.filter(_.token === token).result.headOption)
    val expired : Future[Boolean] = checkSessionValid(session)
    expired.flatMap {
      case true => {
        session.flatMap {
          case Some(s) => val user : Future[Option[UserEntity]] = db.run(users.filter(_.id === s.fields.user_id).result.headOption);
            user.flatMap {
              case Some(u) => Future.successful(u)
              case None => Future.failed(new UserNotFoundException("User associated with this session not found."))
            }
          case None => Future.failed(new SessionNotFoundException("Session not found."))
        }
      }
      case false => {
        Future.failed(new SessionExpiredException("Session expired."))
      }
    }
  }

  def generateSession(updateToken: String) : Future[SessionEntity] = {
    val session : Future[Option[SessionEntity]] = db.run(sessions.filter(_.update_token === updateToken).result.headOption)
    session.flatMap {
      case Some(s) => val session = SessionFactory.create(
        new SessionFields(
          generateToken(),
          generateToken(),
          generateExpiresAt(),
          s.fields.user_id)
        );
      Future.successful(session)
      case None => Future.failed(new SessionNotFoundException("Session with this update token not found."))
    }
  }

  // Get all the series
  def getSessions(): Future[Seq[SessionEntity]] = db.run(sessions.result)

  // Get a series by ID
  def getSessionByID(id: Long): Future[Option[SessionEntity]] = {
    db.run(sessions.filter(_.id === id).result.headOption)
  }

}
