package org.cuappdev.podcast.models.db

// Dependencies
import java.sql.Timestamp

// Internal utilities
import org.cuappdev.podcast.models.SubscriptionEntity
import org.cuappdev.podcast.models.DBInfo
import org.cuappdev.podcast.models.SubscriptionFields
import org.cuappdev.podcast.utils.DatabaseConfig


// Table Entity
trait SubscriptionEntityTable extends DatabaseConfig with UserEntityTable with SeriesEntityTable {

  import driver.api._

  class Subscriptions(tag: Tag) extends Table[SubscriptionEntity](tag, "subscriptions") {

    // Fields of the SQL table
    def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    def created_at = column[Timestamp]("created_at")
    def updated_at = column[Timestamp]("updated_at")
    def user_id = column[Option[Long]]("user_id")
    def user_foreign_key = foreignKey("user_foreign_key", user_id, users)(_.id)
    def series_id = column[Option[Long]]("series_id")
    def series_foreign_key = foreignKey("series_foreign_key", series_id, series)(_.id)

    // Required conversions for reading / writing to / from the DB
    def * = ((id, created_at, updated_at), (user_id, series_id)).shaped <>
      ( {
        case (dbInfo, subscriptionFields) => SubscriptionEntity(DBInfo.tupled.apply(dbInfo), SubscriptionFields.tupled.apply(subscriptionFields))
      }, { s: SubscriptionEntity =>
        def f1(p: DBInfo) = DBInfo.unapply(p).get
        def f2(p: SubscriptionFields) = SubscriptionFields.unapply(p).get
        Some(f1(s.dBInfo), f2(s.fields))
      })
  }

  // Gets subscriptions from the DB
  protected val subscriptions = TableQuery[Subscriptions]

}