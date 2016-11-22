package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SubscriptionsService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SubscriptionFields
import spray.json._
import akka.http.scaladsl.server.Directives._

trait SubscriptionsServiceRoute extends SubscriptionsService with BaseServiceRoute with SecurityDirectives  {
  val subscriptionsRoute = pathPrefix("subscriptions") {

    pathEndOrSingleSlash {                                // /episodes
      get {
        complete(getSubscriptions().map { e => e.toJson })
      } ~
      post {
        entity(as[SubscriptionFields]) { entity =>
          complete(createSubscription(entity).map { e => e.toJson })
        }
      }
    } /* ~ path("l" ~ LongNumber) { id =>
        delete {
          complete(deleteSubscription(id).map { e => e.toJson })
        }
    }  */
  }
}
