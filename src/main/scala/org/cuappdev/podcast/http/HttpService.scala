package org.cuappdev.podcast.http

import org.cuappdev.podcast.http.routes.UsersServiceRoute
import org.cuappdev.podcast.utils.CorsSupport
import akka.http.scaladsl.server.Directives._

trait HttpService extends UsersServiceRoute with CorsSupport {

  val routes =
    pathPrefix("/api/v1") {
      corsHandler {
        usersRoute // ~ otherRoute ~ otherRoute
      }
    }
}
