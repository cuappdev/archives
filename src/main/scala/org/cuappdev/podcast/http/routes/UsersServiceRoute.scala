package org.cuappdev.podcast.http.routes

import com.restfb.DefaultFacebookClient
import com.restfb.FacebookClient.AccessToken
import org.cuappdev.podcast.models.UserEntity
import org.cuappdev.podcast.services.UsersService
import org.cuappdev.podcast.models.SecurityDirectives
import org.cuappdev.podcast.models.routes.BaseServiceRoute
import spray.json._
import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Directives._

trait UsersServiceRoute extends UsersService with BaseServiceRoute with SecurityDirectives {

  import StatusCodes._

  // implicit val usersUpdateFormat = jsonFormat2(UserEntityUpdate)

  // Very basic route
  val usersRoute = pathPrefix("users") {

    pathEndOrSingleSlash {                                // /users
      get {
        complete(getUsers().map { u => u.toJson })
      }
    } ~
      pathPrefix("fb_auth") {                             // /users/fb_auth
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
