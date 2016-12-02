package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SubscriptionsService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SubscriptionFields
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

trait SubscriptionsServiceRoute extends SubscriptionsService with BaseServiceRoute with SecurityDirectives  {
  val subscriptionsRoute = pathPrefix("subscriptions") {

    pathEndOrSingleSlash {                                // /episodes
      get {
        sessionComplete({ user =>
          getSubscriptions().map { e => e.toJson }
        })
      } ~
      post {
        entity(as[SubscriptionFields]) { entity =>
          sessionComplete({ user =>
            createSubscription(entity).map { e => e.toJson }
          })
        }
      }
    } /* ~ path("l" ~ LongNumber) { id =>
        delete {
          complete(deleteSubscription(id).map { e => e.toJson })
        }
    }  */
  }
}
