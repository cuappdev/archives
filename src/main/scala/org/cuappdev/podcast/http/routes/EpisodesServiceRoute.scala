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
        complete(getEpisodes().map { e => e.toJson })
      } ~
      post {
        entity(as[EpisodeFields]) { entity =>
          complete(createEpisode(entity).map { e => e.toJson })
        }
      }
    }


  }
}
