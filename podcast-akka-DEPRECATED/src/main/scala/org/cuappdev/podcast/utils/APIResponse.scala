package org.cuappdev.podcast.utils

import akka.http.scaladsl.marshalling.ToResponseMarshallable
import spray.json.JsObject

/**
  * Response to an API Request
  * @param success - Boolean, indicating whether the request was successful or not
  * @param data - JsObject with the information of the response packaged in
  */
case class APIResponse (success: Boolean, data: JsObject)

/**
  * Functions to help with proper API response formatting
  */
trait APIResponseDirectives {

  /* Utility method */
  def respond (success: Boolean,
               data: JsObject): APIResponse =
    APIResponse (success, data)


}
