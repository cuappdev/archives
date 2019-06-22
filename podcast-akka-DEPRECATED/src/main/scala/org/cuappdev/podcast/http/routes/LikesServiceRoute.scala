package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.LikesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.LikeFields
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

trait LikesServiceRoute extends LikesService with BaseServiceRoute with SecurityDirectives {

}
