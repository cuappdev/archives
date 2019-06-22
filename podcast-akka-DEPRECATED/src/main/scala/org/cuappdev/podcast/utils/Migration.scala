package org.cuappdev.podcast.utils

import java.util.Properties
import org.flywaydb.core.Flyway

/* This trait allows */
trait Migration extends Config {

  private val flyway = new Flyway()
  flyway.setDataSource(databaseUrl, databaseUser, databasePassword)

  def migrate() = {
    flyway.migrate()
  }

  def reloadSchema() = {
    flyway.clean()
    flyway.migrate()
  }

}
