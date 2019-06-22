package org.cuappdev.podcast.models

/* Factory and entity for Subscription. */

case class SubscriptionFields (user_id: Option[Long],
                              series_id: Option[Long]) extends Fields

case class SubscriptionEntity (dBInfo: DBInfo,
                               fields: SubscriptionFields) extends Entity (dBInfo, fields)

object SubscriptionFactory extends EntityFactory[SubscriptionEntity, SubscriptionFields] {

  def instantiate(dbInfo: DBInfo, newFields: SubscriptionFields) = {
    new SubscriptionEntity(dbInfo, newFields)
  }

  def create (f: SubscriptionFields) : SubscriptionEntity = {
    new SubscriptionEntity(DBInfoFactory.create(), f)
  }

  def update (e: SubscriptionEntity, newFields: SubscriptionFields) : SubscriptionEntity = {
    new SubscriptionEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}
