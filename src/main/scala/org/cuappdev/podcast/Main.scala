package org.cuappdev.podcast

import org.cuappdev.podcast.http.HttpServiceRoute
import org.cuappdev.podcast.utils.Config
import org.cuappdev.podcast.utils.Migration

import akka.actor.ActorSystem
import akka.event.{Logging, LoggingAdapter}
import akka.http.scaladsl.Http
import akka.stream.ActorMaterializer
import scala.util.Properties

import scala.concurrent.ExecutionContext

/* Main entrypoint of the app  */
object Main extends App with Config with HttpServiceRoute with Migration {
  private implicit val system = ActorSystem()

  protected implicit val executor: ExecutionContext = system.dispatcher
  protected val log: LoggingAdapter = Logging(system, getClass)
  protected implicit val materializer: ActorMaterializer = ActorMaterializer()

  migrate()
  val port = Properties.envOrElse("PORT", "9000").toInt

  Http().bindAndHandle(routes, interface = "0.0.0.0", port = port)
}
