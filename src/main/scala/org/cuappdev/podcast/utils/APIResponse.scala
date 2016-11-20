package org.cuappdev.podcast.utils

import spray.json.JsObject

/**
  * Response to an API Request
  * @param success - Boolean, indicating whether the request was successful or not
  * @param data - JsObject with the information of the response packaged in
  */
case class APIResponse (success: Boolean, data: JsObject)
