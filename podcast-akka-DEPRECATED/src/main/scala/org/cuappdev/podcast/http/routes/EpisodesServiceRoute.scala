package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.EpisodesService
import org.cuappdev.podcast.models.SecurityDirectives
import akka.http.scaladsl.server.Directives._

trait EpisodesServiceRoute extends EpisodesService
  with BaseServiceRoute with SecurityDirectives {

  val episodesRoute =
    (path ("episodes" / "search") & get) {
      parameters("query") { query =>
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            searchEpisodes(query)
          })
        }}
    } ~
    (path ("episodes" / "related") & get) {
      parameters("id") { id =>
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            relatedEpisodes(id)
          })
        }
      }
    }

}
