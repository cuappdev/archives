package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

// Internal utilities
import org.cuappdev.podcast.models.SessionEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.SessionFields
import org.cuappdev.podcast.utils.DatabaseConfig

// Table Entity
trait SessionEntityTable extends DatabaseConfig {

  import driver.api._

  class Sessions(tag: Tag) extends Table[SessionEntity](tag, "sessions") with UserEntityTable {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    def token = column[String]("token")
    def update_token = column[String]("update_token")
    def expires_at = column[Timestamp]("expires_at")
    def user_id = column[Option[Long]]("user_id")
    def user_foreign_key = foreignKey("user_foreign_key", user_id, users)(_.id)

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (token, update_token, expires_at, user_id)).shaped <>
      ( {
          case (dbInfo, sessionFields) => SessionEntity(DBInfo.tupled.apply(dbInfo), SessionFields.tupled.apply(sessionFields))
      }, { s: SessionEntity =>
          def f1(p: DBInfo) = DBInfo.unapply(p).get
          def f2(p: SessionFields) = SessionFields.unapply(p).get
          Some(f1(s.dBInfo), f2(s.fields))
        })
  }

  // Gets seriess from the DB
  protected val sessions = TableQuery[Sessions]

}
