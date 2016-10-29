package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

// Internal utilities
import org.cuappdev.podcast.models.LikeEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.LikeFields
import org.cuappdev.podcast.utils.DatabaseConfig

// Table Entity
trait LikeEntityTable extends DatabaseConfig {

  import driver.api._

  class Likes(tag: Tag) extends Table[LikeEntity](tag, "likes") {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    // Insert other fields here...

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (/* fields here */)).shaped <>
      ( { case (dbInfo, likeFields) => LikeEntity(DBInfo.tupled.apply(dbInfo), LikeFields.apply(likeFields)) },
        { l: LikeEntity =>
          def f1(p: DBInfo) = DBInfo.unapply(p).get
          def f2(p: LikeFields) = LikeFields.unapply(p).get
          Some(f1(l.dBInfo), f2(l.fields))
        })
  }

  // Gets likes from the DB
  protected val like = TableQuery[Like]

}