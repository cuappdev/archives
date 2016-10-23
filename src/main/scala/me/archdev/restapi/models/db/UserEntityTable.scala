package me.archdev.restapi.models.db

// Dependencies
import java.sql.Timestamp

import org.joda.time.DateTime

// Internal utilities
import me.archdev.restapi.models.UserEntity
import me.archdev.restapi.utils.DatabaseConfig

// Table Entity
trait UserEntityTable extends DatabaseConfig {

  import driver.api._

  class Users(tag: Tag) extends Table[UserEntity](tag, "users") {

    // Fields of the SQL table
    def fb_id = column[String]("fb_id")
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Option[Timestamp]]("created_at", O.Default(Some(new Timestamp(DateTime.now.getMillis))))
    def updated_at = column[Option[Timestamp]]("updated_at", O.Default(Some(new Timestamp(DateTime.now.getMillis))))

    // Required conversions for reading / writing to / from the DB
    def * = (fb_id, id, created_at, updated_at) <> ((UserEntity.apply _).tupled, UserEntity.unapply)

  }

  // Gets users from the DB
  protected val users = TableQuery[Users]


}


