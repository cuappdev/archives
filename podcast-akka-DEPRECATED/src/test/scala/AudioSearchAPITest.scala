import com.typesafe.config.ConfigFactory
import org.scalatest._
import org.cuappdev.podcast.utils.{AudioSearchAPI}


/* Tests for AudioSearchAPI class  */
class AudioSearchAPITest extends FlatSpec {

  /* Loads our configurations */
  val config = ConfigFactory.load()
  /* Grabs audiosearch-specific fields */
  val audiosearchConfig = config.getConfig("audiosearch")
  val audiosearchAppId = audiosearchConfig.getString("app_id")
  val audiosearchSecret = audiosearchConfig.getString("app_secret")
  val audiosearch : AudioSearchAPI = new AudioSearchAPI(audiosearchAppId, audiosearchSecret)

  /* Empty test */
  it should "work" in {}

  /* Successful get */
  it should "make a proper get-request" in {
    val result = audiosearch.searchEpisodes("hello", Map())
  }

  /* Successful refresh */
  it should "refresh + make proper get-request" in {
    audiosearch.accessToken = "garbage"
    val result = audiosearch.get("/search/episodes/hello", Map())
  }

}
