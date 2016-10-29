package me.archdev.restapi.models

import java.sql.Timestamp
import org.joda.time.DateTime

/**
  * Abstract class detailing essential fields for all entities in our API
  * @param id - ID (primary key)
  * @param created_at - Timestamp
  * @param updated_at - Timestamp
  */
abstract case class Entity (id: Option[Long], created_at: Timestamp, updated_at: Timestamp)

/**
  * Blueprint for a Factory for entities
  * @tparam E - Class that extends from the abstract case class Entity
  */
trait EntityFactory[E <: Entity] {

  /**
    * Function to create an entity.
    * @param id - ID of the entity
    * @param created_at - Created timestamp
    * @param updated_at - Updated timestamp
    * @return An Entity instance
    */
  def create (id: Option[Long] = None,
              created_at: Timestamp = new Timestamp(DateTime.now.getMillis),
              updated_at: Timestamp = new Timestamp(DateTime.now.getMillis)) : E = {
    new E(id, created_at, updated_at)
  }

  /**
    * Function to update an entity.
    * @param e - Entity to update
    * @return An Entity instance
    */
  def update (e: E) : E = {
    new E(e.id, e.created_at, new Timestamp(DateTime.now.getMillis))
  }

}
