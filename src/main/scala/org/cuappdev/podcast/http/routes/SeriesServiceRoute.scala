package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SeriesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SeriesFields
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

trait SeriesServiceRoute extends SeriesService with BaseServiceRoute with SecurityDirectives  {
  val seriesRoute = pathPrefix("series") {

    pathEndOrSingleSlash {                                // /likes
      get {
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            getSeries().map { e => e.toJson }
          })
        }
      }
    }

  }
}
