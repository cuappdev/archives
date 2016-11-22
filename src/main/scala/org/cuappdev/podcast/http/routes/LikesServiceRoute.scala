package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.LikesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.LikeFields
import spray.json._
import akka.http.scaladsl.server.Directives._

trait LikesServiceRoute extends LikesService with BaseServiceRoute with SecurityDirectives  {

  val likesRoute = pathPrefix("likes") {

    pathEndOrSingleSlash {                                // /likes
      get {
        complete(getLikes().map { e => e.toJson })
      } ~
      post {
        entity(as[LikeFields]) { entity =>
          complete(createLike(entity).map { e => e.toJson })
        }
      }
    } /* ~ path(LongNumber) { id =>
        delete {
          complete(deleteLike(id).map { e => e.toJson })
        }
    } */

  }
}
