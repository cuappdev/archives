package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SeriesService
import org.cuappdev.podcast.models.SecurityDirectives
import akka.http.scaladsl.server.Directives._

trait SeriesServiceRoute extends SeriesService
  with BaseServiceRoute with SecurityDirectives  {

  val seriesRoute =
    (path ("series" / "search") & get) {
      parameters("query") { query =>
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            searchSeries(query)
          })
        }}
    } ~
    (path ("series" / "related") & get) {
      parameters("id") { id =>
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            relatedSeries(id)
          })
        }
      }
    }

}
