package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

// Internal utilities
import org.cuappdev.podcast.models.UserEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.UserFields
import org.cuappdev.podcast.utils.DatabaseConfig

// Table Entity
trait UserEntityTable extends DatabaseConfig {

  import driver.api._

  class Users(tag: Tag) extends Table[UserEntity](tag, "users") {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    def fb_id = column[String]("fb_id")

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (fb_id)).shaped <>
      ( { case (dbInfo, userFields) => UserEntity(DBInfo.tupled.apply(dbInfo), UserFields.apply(userFields)) },
        { u: UserEntity =>
          def f1(p: DBInfo) = DBInfo.unapply(p).get
          def f2(p: UserFields) = UserFields.unapply(p).get
          Some(f1(u.dBInfo), f2(u.fields))
        })
  }

  // Gets users from the DB
  protected val users = TableQuery[Users]

}


