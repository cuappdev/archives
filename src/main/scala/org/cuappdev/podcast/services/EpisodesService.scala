package org.cuappdev.podcast.services

import org.cuappdev.podcast.models.db.EpisodeEntityTable
import org.cuappdev.podcast.models.{EpisodeEntity, EpisodeFactory, EpisodeFields}
import org.cuappdev.podcast.utils.{AudioSearch, Config}
import spray.json.{JsArray, JsNumber, JsObject, JsString, JsValue}

// Execution requirements
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

object EpisodesService extends EpisodesService

case class EpisodeNotFoundException(msg: String) extends Exception(msg: String)

trait EpisodesService extends EpisodeEntityTable with Config {

  /* Necessary */
  import driver.api._


  /* Search episodes via a query */
  def searchEpisodes (query: String): Seq[EpisodeEntity] = {
    /* Grab API response */
    val eps : JsArray = AudioSearch.getInstance.searchEpisodes(query, Map())
                                    .asJsObject.fields("results").asInstanceOf[JsArray]
    /* Build result */
    val result = eps.elements.map(jsonVal => {
      val json = jsonVal.asJsObject
      val audiosearchID = json.fields("id").asInstanceOf[JsNumber].value.longValue()
      val title = json.fields("title").asInstanceOf[JsString].value
      val description = json.fields.get("description") match { case None => "" case Some(d) => d.asInstanceOf[JsString].value }
      val audioURL = json.fields("audio_files").asInstanceOf[JsArray]
                         .elements.apply(0).asJsObject.fields("mp3").asInstanceOf[JsString].value
      val imageURL = json.fields("image_urls").asJsObject.fields("full").asInstanceOf[JsString].value
      EpisodeFactory.create(EpisodeFields(audiosearchID, title, description, audioURL, imageURL, None))
    })
    result
  }







}
