package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SubscriptionsService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SubscriptionFields
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

trait SubscriptionsServiceRoute extends SubscriptionsService with BaseServiceRoute with SecurityDirectives  {

}
