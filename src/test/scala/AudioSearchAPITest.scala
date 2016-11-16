import com.typesafe.config.ConfigFactory
import org.scalatest._
import org.cuappdev.podcast.utils.AudioSearchAPI


/* Tests for AudioSearchAPI class  */
class AudioSearchAPITest extends FlatSpec {

  /* Loads our configurations */
  val config = ConfigFactory.load()
  /* Grabs audiosearch-specific fields */
  val audiosearchConfig = config.getConfig("audiosearch")
  val audiosearchAppId = audiosearchConfig.getString("app_id")
  val audiosearchSecret = audiosearchConfig.getString("app_secret")

  /* Beginning test */
  it should "work" in {
    val audiosearch : AudioSearchAPI = new AudioSearchAPI(audiosearchAppId, audiosearchSecret)
  }









}
