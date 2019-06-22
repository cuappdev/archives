package org.cuappdev.podcast.http

import org.cuappdev.podcast.http.routes._
import org.cuappdev.podcast.services.HttpService
import org.cuappdev.podcast.utils.CorsSupport
import akka.http.scaladsl.server.Directives.{pathEndOrSingleSlash, _}


trait HttpServiceRoute extends UsersServiceRoute with EpisodesServiceRoute
  with LikesServiceRoute with SeriesServiceRoute with SubscriptionsServiceRoute
  with HttpService with CorsSupport {

  val routes =
    pathPrefix("v1") {
      corsHandler {
        usersRoute ~ episodesRoute ~ seriesRoute
      } ~
      (path("search") & get) {
        parameters("query") { query =>
          headerValueByName("SESSION_TOKEN") { session =>
            sessionComplete(session, { user =>
              searchEverything(query)
            })
          }
        }
      }

    }
}
