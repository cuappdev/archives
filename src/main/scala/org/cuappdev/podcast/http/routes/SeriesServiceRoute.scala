package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SeriesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SeriesFields
import spray.json._
import akka.http.scaladsl.server.Directives._

trait SeriesServiceRoute extends SeriesService with BaseServiceRoute with SecurityDirectives  {
  val seriesRoute = pathPrefix("series") {

    pathEndOrSingleSlash {                                // /likes
      get {
        complete(getSeries().map { e => e.toJson })
      } ~
      post {
        entity(as[SeriesFields]) { entity =>
          complete(createSeries(entity).map { e => e.toJson })
        }
      }
    }

  }
}
