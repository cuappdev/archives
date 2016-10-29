package org.cuappdev.podcast.http

import org.cuappdev.podcast.utils.CorsSupport

trait HttpService extends UsersServiceRoute with CorsSupport {

  val routes =
    pathPrefix("/api/v1") {
      corsHandler {
        usersRoute // ~ otherRoute ~ otherRoute
      }
    }
}
