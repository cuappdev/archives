package org.cuappdev.utils

import com.typesafe.config.ConfigFactory

/* Defines fields for various configurations of the app  */
trait Config {
  // Grabs the scope of application.conf
  val config = ConfigFactory.load()

  // Grabs specific config groupings from application.conf
  val httpConfig = config.getConfig("http")
  val databaseConfig = config.getConfig("database")
  val facebookConfig = config.getConfig("facebook")
  val audiosearchConfig = config.getConfig("audiosearch")

  // Grabs fields of HTTP config
  val httpInterface = httpConfig.getString("interface")
  val httpPort = httpConfig.getInt("port")

  // Grabs fields of the DB config
  val databaseUrl = databaseConfig.getString("url")
  val databaseUser = databaseConfig.getString("user")
  val databasePassword = databaseConfig.getString("password")

  // Grabs facebook-specific fields
  val facebookAppId = facebookConfig.getString("app_id")
  val facebookSecret = facebookConfig.getString("app_secret")

  // Grabs audiosearch-specific fields
  val audiosearchAppId = audiosearchConfig.getString("app_id")
  val audiosearchSecret = audiosearchConfig.getString("app_secret")

}
