package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.utils.Config
import org.cuappdev.podcast.utils.Protocol
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport
import akka.stream.ActorMaterializer
import org.cuappdev.podcast.services.SessionsService._
import org.cuappdev.podcast.models.UserEntity
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.StandardRoute
import org.cuappdev.podcast.services.UserNotFoundException
import org.cuappdev.podcast.utils.APIResponseDirectives
import spray.json._

import scala.concurrent.Future
import scala.util.{Failure, Success}
import scala.concurrent.ExecutionContext

trait BaseServiceRoute extends Protocol with SprayJsonSupport with Config with APIResponseDirectives {
  protected implicit def executor: ExecutionContext
  protected implicit def materializer: ActorMaterializer
  protected def log: LoggingAdapter

  /** Session completion **/
  protected def sessionComplete(sessionToken: String,
                                func : (UserEntity => JsValue)) : StandardRoute = {
    complete(grabUserBySessionToken(sessionToken).map { u => func(u) })
  }

}
