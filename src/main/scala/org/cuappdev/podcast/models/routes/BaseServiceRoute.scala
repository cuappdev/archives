package org.cuappdev.podcast.models.routes

import me.archdev.restapi.utils.Config
import org.cuappdev.podcast.utils.Protocol

import scala.concurrent.ExecutionContext

trait BaseServiceRoute extends Protocol with SprayJsonSupport with Config {
  protected implicit def executor: ExecutionContext
  protected implicit def materializer: ActorMaterializer
  protected def log: LoggingAdapter
}
