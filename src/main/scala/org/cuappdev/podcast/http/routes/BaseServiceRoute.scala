package org.cuappdev.podcast.http.routes

import org.cuappdev.podcast.utils.Config
import org.cuappdev.podcast.utils.Protocol
import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport
import akka.stream.ActorMaterializer
import org.cuappdev.podcast.services.SessionsService

import scala.concurrent.ExecutionContext

trait BaseServiceRoute extends Protocol with SprayJsonSupport with Config {
  protected implicit def executor: ExecutionContext
  protected implicit def materializer: ActorMaterializer
  protected def log: LoggingAdapter

  protected def sessionComplete(func) = {
    headerValueByName("SESSION_TOKEN") { sessionToken =>
      grabSuccess = grabUserBySessionToken(sessionToken)
      grabSuccess.flatMap {
        case Success(u) => complete(func(u))
        case Failure(ex : SessionExpiredException) =>
          headerValueByName("UPDATE_TOKEN") { updateToken =>
            generateSuccess = generateSession(updateToken)
            generateSuccess.flatMap {
              case Success(s) => grabCreatedSuccess = grabUserBySessionToken(s.fields.token)
                  grabCreatedSuccess.flatMap {
                    case Success(u) => complete(func(u))
                    case Failure(_) => "Something went wrong."
                  }
            }
          }
        case Failure(_) => "Something went wrong."
      }
    }
  }
}
