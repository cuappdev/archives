package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

// Internal utilities
import org.cuappdev.podcast.models.SeriesEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.SeriesFields
import org.cuappdev.podcast.utils.DatabaseConfig

// Table Entity
trait SeriesEntityTable extends DatabaseConfig {

  import driver.api._

  class Seriess(tag: Tag) extends Table[SeriesEntity](tag, "seriess") {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    def audiosearch_id = column[Long]("audiosearch_id")
    def title = column[String]("title")
    def description = column[String]("description")
    def imageUrl = column[String]("imageUrl")

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (audiosearch_id, title, description, imageUrl).shaped <>
      ( { case (dbInfo, seriesFields) => SeriesEntity(DBInfo.tupled.apply(dbInfo), SeriesFields.apply(seriesFields)) },
        { s: SeriesEntity =>
          def f1(p: DBInfo) = DBInfo.unapply(p).get
          def f2(p: SeriesFields) = SeriesFields.unapply(p).get
          Some(f1(s.dBInfo), f2(s.fields))
        })
  }

  // Gets seriess from the DB
  protected val series = TableQuery[Series]

}