package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.SeriesEntityTable
import org.cuappdev.podcast.models.{SeriesEntity, SeriesFields, SeriesFactory}
import org.cuappdev.podcast.utils.Config

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object SeriesService extends SeriesService

trait SeriesService extends SeriesEntityTable with Config {

  import driver.api._

  // Get all the series
  def getSeries(): Future[Seq[SeriesEntity]] = db.run(series.result)

  // Get a series by ID
  def getSeriesByID(id: Long): Future[Option[SeriesEntity]] = {
    db.run(series.filter(_.id === id).result.headOption)
  }

}
