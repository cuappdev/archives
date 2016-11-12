package org.cuappdev.podcast.http

import org.cuappdev.podcast.http.routes._
import org.cuappdev.podcast.utils.CorsSupport
import akka.http.scaladsl.server.Directives._

trait HttpService extends UsersServiceRoute with EpisodesServiceRoute with LikesServiceRoute with CorsSupport {

  val routes =
    pathPrefix("v1") {
      corsHandler {
        usersRoute ~ episodesRoute
      }
    }
}
