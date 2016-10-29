package org.cuappdev.podcast.models

/* Factory and entity for Subscription. */

case class SubscriptionFields (
                                /* define fields here */
                              ) extends Fields

case class SubscriptionEntity (dBInfo: DBInfo,
                               fields: SubscriptionFields) extends Entity (dBInfo, fields)

object SubscriptionFactory extends EntityFactory[SubscriptionEntity, SubscriptionFields] {

  def create (f: SubscriptionFields) : SubscriptionEntity = {
    new SubscriptionEntity(DBInfoFactory.create(), f)
  }

  def update (e: SubscriptionEntity, newFields: SubscriptionFields) : SubscriptionEntity = {
    new SubscriptionEntity(DBInfoFactory.update(e.dBInfo), newFields)
  }

}
