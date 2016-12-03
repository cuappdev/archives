package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.EpisodesService
import org.cuappdev.podcast.models.SecurityDirectives
import spray.json._
import akka.http.scaladsl.server.Directives._
import org.cuappdev.podcast.utils.APIResponseDirectives
import scala.concurrent.Future

trait EpisodesServiceRoute extends EpisodesService
  with BaseServiceRoute with SecurityDirectives with APIResponseDirectives {

  val episodesRoute = pathPrefix("episodes") {
    pathEndOrSingleSlash {
      /* /episodes */
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
        pathEndOrSingleSlash {                            /* /episodes/search?query={query} */
          get {
            parameters("query") { query =>
              headerValueByName("SESSION_TOKEN") { session =>
                sessionComplete(session, { user =>
                  respond(success=true,
                    data=JsObject("episodes" ->
                      JsArray(searchEpisodes(query).map { ep => ep.toJson }.toVector)))
                    .toJson})
              }}
            }
          }
        }
      } ~ {
        pathPrefix("related") {
          pathEndOrSingleSlash {                            /* /episodes/related?id={id} */
            get {
              parameters("id") { id =>
                headerValueByName("SESSION_TOKEN") { session =>
                  sessionComplete(session, { user =>
                    respond(
                      success=true,
                      data=JsObject("episodes" ->
                        JsArray(relatedEpisodes(Integer.parseInt(id)).map { ep => ep.toJson }.toVector)))
                      .toJson
                  })
                }
              }
            }
          }
        }

    }
  }
}
