package me.archdev.restapi.models

// Java representation of the timestamp
import java.sql.Timestamp

import org.joda.time.DateTime

case class UserEntity(fb_id: String,
                      id: Option[Long] = None,
                      created_at: Option[Timestamp] = Some(new Timestamp(DateTime.now.getMillis)),
                      updated_at: Option[Timestamp] = Some(new Timestamp(DateTime.now.getMillis))) {

  // Perform validations in here

}

// case class UserEntityUpdate ... TODO


