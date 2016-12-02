package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.services.UsersService
import org.cuappdev.podcast.models.SecurityDirectives
import spray.json._
import akka.http.scaladsl.server.Directives._
import scala.concurrent.Future

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
              complete(getOrCreateUser(fb_token).map { u => u.toJson })
            }
          }
        }
      }
  }

}
