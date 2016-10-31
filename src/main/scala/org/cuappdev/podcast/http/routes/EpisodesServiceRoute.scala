package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.EpisodesService
import org.cuappdev.podcast.models.SecurityDirectives
import akka.http.scaladsl.server.Directives._

trait EpisodesServiceRoute extends EpisodesService with BaseServiceRoute with SecurityDirectives  {
  val episodesRoute = pathPrefix("episodes") {

    pathEndOrSingleSlash {                                // /users
      get {
        complete(getEpisodes().map { e => e.toJson })
      }
    }


  }
}
