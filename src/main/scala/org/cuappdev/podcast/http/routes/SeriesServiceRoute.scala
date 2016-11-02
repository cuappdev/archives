package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SeriesService
import org.cuappdev.podcast.models.SecurityDirectives
import spray.json._
import akka.http.scaladsl.server.Directives._

trait SeriesServiceRoute extends SeriesService with BaseServiceRoute with SecurityDirectives  {
  /*
  val SeriesRoute = pathPrefix("Series") {

    pathEndOrSingleSlash {                                // /Series
      get {
        complete(getSeries().map { s => s.toJson })
      }
    }

  }
  */
}
