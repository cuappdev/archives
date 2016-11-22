package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.EpisodesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.EpisodeFields
import spray.json._
import akka.http.scaladsl.server.Directives._

trait EpisodesServiceRoute extends EpisodesService with BaseServiceRoute with SecurityDirectives  {

  val episodesRoute = pathPrefix("episodes") {

    pathEndOrSingleSlash {                                // /episodes
      get {
        complete(getEpisodes())
      }
    } /* ~ pathPrefix(IntNumber) { id =>
        delete {
          complete(deleteEpisode(id).map { e => e.toJson })
        }
      } */

  }
}
