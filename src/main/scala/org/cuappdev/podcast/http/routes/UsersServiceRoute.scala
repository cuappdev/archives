package org.cuappdev.podcast.http.routes

import java.lang

import org.cuappdev.podcast.services.{SessionNotFoundException, SessionsService, UsersService}
import org.cuappdev.podcast.models.{SecurityDirectives, SessionEntity}
import spray.json._
import akka.http.scaladsl.server.Directives._

import scala.concurrent.Future
import scala.util.control

trait UsersServiceRoute extends UsersService with BaseServiceRoute with SecurityDirectives {

  // Very basic route
  val usersRoute = pathPrefix("users") {

    pathEndOrSingleSlash {                                /* /users */
      get {
        sessionComplete({ user =>
          getUsers().map { u => u.toJson }
        })
      }
    } ~
      pathPrefix("fb_auth") {                             /* /users/fb_auth */
        pathEndOrSingleSlash {
          post {
            // Grab the header + respond
            headerValueByName("FB_TOKEN") { fb_token =>
              getOrCreateUser(fb_token).map {
                case Some(u) =>
                  val session = SessionsService.sessionFromUser(u)
                  val userJSON = u.toJson
                  val sessionJSON = session.map {
                    case Some (s) => s.toJson
                    case None => SessionNotFoundException("Session not found by that token.")
                  }
                  respond(success = true,
                    data = JsObject(Map("session" -> sessionJSON,
                                        "user"    -> userJSON)).toJson
                case None =>
                  respond(success = false,
                    data = JsObject("error" -> "Something went wrong")).toJson
              }
            }
          }
        }
      }
  }

}
