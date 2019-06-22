package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.SubscriptionEntityTable
import org.cuappdev.podcast.models.{SubscriptionFields, SubscriptionEntity, SubscriptionFactory}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object SubscriptionsService extends SubscriptionsService

case class SubscriptionNotFoundException(msg: String) extends Exception(msg: String)

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

  /**
    * Deletes a subscription.
    * @param id the ID of the subscription to delete
    * @return the ID of the deleted subscription
    */
  def deleteSubscription(id: Long) : Future[Option[Long]] = {
    val e : Future[Option[SubscriptionEntity]] = getSubscriptionByID(id)
    e.flatMap {
      case Some(entity) => {
        db.run(subscriptions.filter(_.id === id).delete)
        Future.successful(Some(id)) }
      case None => Future.failed(new SubscriptionNotFoundException("Like not found"))
    }
  }

}
