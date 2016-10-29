package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

import com.restfb.types.Conversation.Tag
import slick.model.Table

// Internal utilities
import org.cuappdev.podcast.models.EpisodeEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.EpisodeFields
import org.cuappdev.podcast.utils.DatabaseConfig

// Table Entity
trait EpisodeEntityTable extends DatabaseConfig {

  import driver.api._

  class Episodes(tag: Tag) extends Table[EpisodeEntity](tag, "episodes") {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    // Insert other fields here...

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (/* fields here */)).shaped <>
      ( { case (dbInfo, episodeFields) => EpisodeEntity(DBInfo.tupled.apply(dbInfo), EpisodeFields.apply(episodeFields)) },
        { e: EpisodeEntity =>
          def f1(p: DBInfo) = DBInfo.unapply(p).get
          def f2(p: EpisodeFields) = EpisodeFields.unapply(p).get
          Some(f1(e.dBInfo), f2(e.fields))
        })
  }

  // Gets episodes from the DB
  protected val episode = TableQuery[Episode]

}