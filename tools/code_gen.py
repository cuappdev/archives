def generate_factory_code(obj_name):
  return """
  package org.cuappdev.podcast.models

  /* Factory and entity for {}. */

  case class {}Fields (
    /* define fields here */
  ) extends Fields

  case class {}Entity (override val dBInfo: DBInfo,
                       override val fields: {}Fields) extends Entity (dBInfo, fields)

  object {}Factory extends EntityFactory[{}Entity, {}Fields] {

    def create (f: {}Fields) : {}Entity = {
      new {}Entity(DBInfoFactory.create(), f)
    }

    def update (e: {}Entity, newFields: {}Fields) : {}Entity = {
      new {}Entity(DBInfoFactory.update(e.dBInfo), newFields)
    }

  }""".replace("{}", obj_name)


if __name__ == "__main__":
    print generate_factory_code("Series")
    print generate_factory_code("Episode")
    print generate_factory_code("Like")
    print generate_factory_code("Subscription")
