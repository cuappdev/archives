package org.cuappdev.podcast.http.routes

import java.lang

import org.cuappdev.podcast.services.{SessionNotFoundException, SessionsService, UserErrorException, UsersService}
import org.cuappdev.podcast.models.{SecurityDirectives, SessionEntity}
import spray.json._
import akka.http.scaladsl.server.Directives._
import org.omg.CORBA.UserException

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
            /* Grab the header + respond */
            headerValueByName("FB_TOKEN") { fb_token =>
              /* Get the user */
              complete(getOrCreateUser(fb_token).map {
                case (futureU, futureS) =>
                  respond(success = true,
                    data = JsObject("session" -> futureU.toJson,
                                    "user" -> futureS.toJson)).toJson
                case _ => UserErrorException("An error occurred")
              }.toJson)
            }
          }
        }
      }
  }

}
