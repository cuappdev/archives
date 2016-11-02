package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SubscriptionsService
import org.cuappdev.podcast.models.SecurityDirectives
import spray.json._
import akka.http.scaladsl.server.Directives._

trait SubscriptionsServiceRoute extends SubscriptionsService with BaseServiceRoute with SecurityDirectives  {
  /*
  val subscriptionsRoute = pathPrefix("subscriptions") {

    pathEndOrSingleSlash {                                // /subscriptions
      get {
        complete(getSubscriptions().map { s => s.toJson })
      }
    }

  }
  */
}