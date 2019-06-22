# Usage: python tools/code_gen.py >> file.scala

# Models

def generate_factory_code(obj_name):
  return """
  package org.cuappdev.podcast.models

  /* Factory and entity for {}. */

  case class {}Fields (
	/* define fields here */
  ) extends Fields

  case class {}Entity (dBInfo: DBInfo,
					  fields: {}Fields) extends Entity (dBInfo, fields)

  object {}Factory extends EntityFactory[{}Entity, {}Fields] {

	def create (f: {}Fields) : {}Entity = {
	  new {}Entity(DBInfoFactory.create(), f)
	}

	def update (e: {}Entity, newFields: {}Fields) : {}Entity = {
	  new {}Entity(DBInfoFactory.update(e.dBInfo), newFields)
	}

  }""".replace("{}", obj_name)

def generate_db_table_code(obj_name):
  return """
    package org.cuappdev.podcast.models.db

    // Dependencies
    import java.sql.Timestamp

    // Internal utilities
    import org.cuappdev.podcast.models.{1}Entity
    import org.cuappdev.podcast.models.DBInfo
    import org.cuappdev.podcast.models.{1}Fields
    import org.cuappdev.podcast.utils.DatabaseConfig

    // Table Entity
    trait {1}EntityTable extends DatabaseConfig {

      import driver.api._

      class {1}s(tag: Tag) extends Table[{1}Entity](tag, "{2}s") {

    	// Fields of the SQL table
    	def id = column[Option[Long]]("id", O.PrimaryKey, O.AutoInc)
    	def created_at = column[Timestamp]("created_at")
    	def updated_at = column[Timestamp]("updated_at")
    	// Insert other fields here...

    	// Required conversions for reading / writing to / from the DB
    	def * = ((id, created_at, updated_at), (/* fields */)).shaped <>
    	  ( { case (dbInfo, {2}Fields) => {1}Entity(DBInfo.tupled.apply(dbInfo), {1}Fields.apply({2}Fields)) },
    		{ {3}: {1}Entity =>
    		  def f1(p: DBInfo) = DBInfo.unapply(p).get
    		  def f2(p: {1}Fields) = {1}Fields.unapply(p).get
    		  Some(f1({3}.dBInfo), f2({3}.fields))
    		})
      }

      // Gets {2}s from the DB
      protected val {2}s = TableQuery[{1}]

    }
  """.replace("{1}", obj_name).replace("{2}", obj_name.lower()).replace("{3}", obj_name.lower()[0])

# Controllers

def generate_service_code(obj_name):
    return """
    package org.cuappdev.podcast.services

    import org.cuappdev.podcast.models.db.{1}EntityTable
    import org.cuappdev.podcast.models.{1}Entity
    import org.cuappdev.podcast.utils.Config

    import scala.concurrent.Future

    object {1}sService extends {1}sService

    trait {1}sService extends {1}EntityTable with Config {

      import driver.api._

      // Get all the episodes
      def get{1}s(): Future[Seq[{1}Entity]] = db.run({2}.result)


      // Get an episode by ID
      def getByID(id: Long): Future[Option[{1}Entity]] = {
        db.run({2}s.filter(_.id == id).result.headOption)
      }


    }
    """.replace("{1}", obj_name).replace("{2}", obj_name.lower())

def generate_service_route_code(obj_name):
    return """
    package org.cuappdev.podcast.http.routes

    import org.cuappdev.podcast.services.{1}sService
    import org.cuappdev.podcast.models.SecurityDirectives
    import spray.json._
    import akka.http.scaladsl.server.Directives._

    trait {1}sServiceRoute extends {1}sService with BaseServiceRoute with SecurityDirectives  {

      val {2}sRoute = pathPrefix("{2}s") {

        pathEndOrSingleSlash {                                // /{2}s
          get {
            complete(get{1}s().map { {3} => {3}.toJson })
          }
        }

      }
    }""".replace("{1}", obj_name).replace("{2}", obj_name.lower()).replace("{3}", obj_name.lower()[0])



if __name__ == "__main__":
    for obj_name in ["Series", "Episode", "Like", "Subscription"]:
        # print generate_factory_code(obj_name)
        # print generate_db_table_code(obj_name)
        print generate_service_code(obj_name)
        print generate_service_route_code(obj_name)
