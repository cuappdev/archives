package org.cuappdev.podcast.utils

trait DatabaseConfig {
  val driver = slick.driver.PostgresDriver

  import driver.api._

  // Grab the db
  def db = Database.forConfig("database")

  // Establish a session to interact with the DB
  implicit val session: Session = db.createSession()
}
