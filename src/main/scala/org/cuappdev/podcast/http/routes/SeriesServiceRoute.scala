package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.SeriesService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.SeriesFields
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

trait SeriesServiceRoute extends SeriesService with BaseServiceRoute with SecurityDirectives  {

  val seriesRoute = pathPrefix("series") {
    pathEndOrSingleSlash {
      /* /series */
      get {
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            respond(success = true,
              data = JsObject()).toJson
          })
        }
      }
    } ~ {
      pathPrefix("search") {
        pathEndOrSingleSlash {                            /* /series/search?query={query} */
          get {
            parameters("query") { query =>
              headerValueByName("SESSION_TOKEN") { session =>
                sessionComplete(session, { user =>
                  searchSeries(query)
                })
              }}
          }
        }
      }
    } ~ {
      pathPrefix("related") {
        pathEndOrSingleSlash {                            /* /series/related?id={id} */
          get {
            parameters("id") { id =>
              headerValueByName("SESSION_TOKEN") { session =>
                sessionComplete(session, { user =>
                  relatedSeries(id)
                })
              }
            }
          }
        }
      }
    }
  }
}
