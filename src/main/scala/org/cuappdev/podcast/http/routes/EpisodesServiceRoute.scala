package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.EpisodesService
import org.cuappdev.podcast.models.{EpisodeFields, SecurityDirectives}
import spray.json._
import akka.http.scaladsl.server.Directives._

trait EpisodesServiceRoute extends EpisodesService with BaseServiceRoute with SecurityDirectives  {

  import org.cuappdev.podcast.utils.Protocol._;

  val episodesRoute = pathPrefix("episodes") {

    pathEndOrSingleSlash {                                // /episodes
      get {
        complete(getEpisodes().map { e => e.toJson })
      }
      post {
        entity(as[EpisodeFields]) { entity =>
          complete(createEpisode(entity).map { e => "OK" })
        }
      }
    }


  }
}
