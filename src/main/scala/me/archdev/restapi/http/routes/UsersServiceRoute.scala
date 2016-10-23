package me.archdev.restapi.http.routes

import akka.http.scaladsl.model.StatusCodes
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.PathMatchers.IntNumber
import com.restfb.DefaultFacebookClient
import com.restfb.FacebookClient.AccessToken
import me.archdev.restapi.http.SecurityDirectives
import me.archdev.restapi.models.UserEntity
import me.archdev.restapi.services.UsersService
import spray.json._

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
              println(fb_token)
              complete(getOrCreateUser(fb_token))
            }
          }
        }
      }


  }

}
