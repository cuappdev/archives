package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.utils.Config
import org.cuappdev.podcast.utils.Protocol
import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport
import akka.stream.ActorMaterializer
import org.cuappdev.podcast.services.SessionsService._
import org.cuappdev.podcast.models.UserEntity
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.StandardRoute
import org.cuappdev.podcast.utils.APIResponse
import org.cuappdev.podcast.utils.APIResponseDirectives
import spray.json._
import scala.concurrent.Future
import scala.util.{Success, Failure}

import scala.concurrent.ExecutionContext

trait BaseServiceRoute extends Protocol with SprayJsonSupport with Config with APIResponseDirectives {
  protected implicit def executor: ExecutionContext
  protected implicit def materializer: ActorMaterializer
  protected def log: LoggingAdapter

  protected def sessionComplete(func : (UserEntity => Future[JsValue])) : Future[StandardRoute] = {
    headerValueByName("SESSION_TOKEN") { sessionToken =>
      val grabSuccess = grabUserBySessionToken(sessionToken)
      grabSuccess.flatMap {
        case Some(u) => Future.successful(complete(func(u)))
        case None =>
          headerValueByName("UPDATE_TOKEN") { updateToken =>
            val generateSuccess = updateSession(updateToken)
            generateSuccess.flatMap {
              case Some(s) => val grabCreatedSuccess = grabUserBySessionToken(s.fields.token)
                grabCreatedSuccess.flatMap {
                  case Some(u) => Future.successful(complete(func(u)))
                  case None => Future.successful(complete(respond(success=false,
                    JsObject("errors" -> JsArray(JsString("Unable to create session.")))).toJson))
                }
            }
          }
        }
      }
  }
}
