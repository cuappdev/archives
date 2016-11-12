package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.LikesService
import org.cuappdev.podcast.models.SecurityDirectives
import spray.json._
import akka.http.scaladsl.server.Directives._

trait LikesServiceRoute extends LikesService with BaseServiceRoute with SecurityDirectives  {

  /*
  val likesRoute = pathPrefix("likes") {
    pathEndOrSingleSlash {                                // /likes
      get {
        complete(getLikes().map { l => l.toJson })
      }
      post {
        entity(as[LikeFields]) { entity =>
          complete(createLikes(entity).map { e => "OK" })
        }
      }
    }
  } */
}
