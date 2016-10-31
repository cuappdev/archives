package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.SubscriptionEntityTable
import org.cuappdev.podcast.models.SubscriptionEntity
import org.cuappdev.podcast.utils.Config

import scala.concurrent.Future

object SubscriptionsService extends SubscriptionsService

trait SubscriptionsService extends SubscriptionEntityTable with Config {

  import driver.api._

  // Get all the episodes
  def getSubscriptions(): Future[Seq[SubscriptionEntity]] = db.run(subscription.result)


  // Get an episode by ID
  def getByID(id: Long): Future[Option[SubscriptionEntity]] = {
    db.run(subscriptions.filter(_.id == id).result.headOption)
  }


}
