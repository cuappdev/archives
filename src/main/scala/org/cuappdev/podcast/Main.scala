package org.cuappdev.podcast

import me.archdev.restapi.utils.Config
import org.cuappdev.podcast.utils.Migration

import scala.concurrent.ExecutionContext

/* Main entrypoint of the app  */
object Main extends App with Config with HttpService with Migration {
  private implicit val system = ActorSystem()

  override protected implicit val executor: ExecutionContext = system.dispatcher
  override protected val log: LoggingAdapter = Logging(system, getClass)
  override protected implicit val materializer: ActorMaterializer = ActorMaterializer()

  migrate()

  Http().bindAndHandle(routes, httpInterface, httpPort)
}
