package org.cuappdev.podcast.models

import akka.http.scaladsl.server.directives.{ RouteDirectives, BasicDirectives, HeaderDirectives, FutureDirectives }

trait SecurityDirectives {

  import BasicDirectives._
  import HeaderDirectives._
  import RouteDirectives._
  import FutureDirectives._

  /*
  def authenticate: Directive1[UserEntity] = {
    headerValueByName("Token").flatMap { token =>
      onSuccess(AuthService.authenticate(token)).flatMap {
        case Some(user) => provide(user)
        case None       => reject
      }
    }
  }
  */

}
