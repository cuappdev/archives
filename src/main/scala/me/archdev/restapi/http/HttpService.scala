package me.archdev.restapi.http

import akka.http.scaladsl.server.Directives._
import me.archdev.restapi.http.routes._
import me.archdev.restapi.utils.CorsSupport

trait HttpService extends UsersServiceRoute with CorsSupport {

  val routes =
    pathPrefix("v1") {
      corsHandler {
        usersRoute // ~ otherRoute ~ otherRoute
      }
    }
}
