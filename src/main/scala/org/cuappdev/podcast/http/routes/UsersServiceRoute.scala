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
        headerValueByName("SESSION_TOKEN") { session =>
          sessionComplete(session, { user =>
            respond(success = true, data = JsNull.asJsObject).toJson
          })
        }
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
                  futureS.map { s =>
                    futureU.map { u =>
                      (s, u) match {
                        case (Some(s1), Some(u1)) =>
                          respond(success = true,
                          data = JsObject("session" -> s1.toJson,
                                          "user" -> u1.toJson)).toJson
                        case _ => SessionNotFoundException("An error occurred.")
                      }

                    }
                  }
                case _ => UserErrorException("An error occurred.")
              }.asInstanceOf[Future[Future[Future[JsValue]]]])
            }
          }
        }
      }
  }

}
