package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.SubscriptionEntityTable
import org.cuappdev.podcast.models.{SubscriptionFields, SubscriptionEntity, SubscriptionFactory}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object SubscriptionsService extends SubscriptionsService

trait SubscriptionsService extends SubscriptionEntityTable with Config {

  import driver.api._

  // Get all the episodes
  def getSubscriptions(): Future[Seq[SubscriptionEntity]] = db.run(subscriptions.result)

  // Get an episode by ID
  def getSubscriptionByID(id: Long): Future[Option[SubscriptionEntity]] = {
    db.run(subscriptions.filter(_.id === id).result.headOption)
  }

  /**
    * Creates a new subscription given some fields.
    * @param fields the SubscriptionFields needed to create the SubscriptionEntity
    * @return the newly created SubscriptionEntity
    */
  def createSubscription(fields : SubscriptionFields): Future[Option[SubscriptionEntity]] = {
    val newSubscription = SubscriptionFactory.create(fields)
    db.run(subscriptions returning subscriptions += newSubscription)
    Future.successful(Some(newSubscription))
  }

}
