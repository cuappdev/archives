package podcast.repos;

import com.couchbase.client.java.Bucket;
import com.couchbase.client.java.document.JsonDocument;
import com.couchbase.client.java.query.N1qlQuery;
import com.couchbase.client.java.query.N1qlQueryRow;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import podcast.models.entities.podcasts.Episode;
import podcast.models.entities.recommendations.Recommendation;
import podcast.models.entities.users.User;
import rx.Observable;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;
import static com.couchbase.client.java.query.Select.select;
import static com.couchbase.client.java.query.dsl.Expression.*;
import static podcast.utils.Constants.*;

@Component
public class RecommendationsRepo {

  private Bucket bucket;

  @Autowired
  public RecommendationsRepo(@Qualifier("dbBucket") Bucket bucket) {
    this.bucket = bucket;
  }

  /** Stores a recommendation */
  public Recommendation storeRecommendation(Recommendation recommendation,
                                            Episode episode) {
    bucket.upsert(recommendation.toJsonDocument());
    return recommendation;
  }

  /** Deletes a recommendation */
  public Recommendation deleteRecommendation(Recommendation recommendation,
                                      Episode episode) {
    if (recommendation == null) return null;
    bucket.remove(Recommendation.composeKey(recommendation));
    return recommendation;
  }

  /** Get a recommendation by user and episodeId */
  public Recommendation getRecommendation(User user, String episodeId) {
    JsonDocument doc = bucket.get(Recommendation.composeKey(episodeId, user.getId()));
    if (doc == null) {
      return null;
    } else {
      return new Recommendation(doc.content());
    }
  }

  /** Get a user's recommendations */
  public List<Recommendation> getUserRecommendations(User user) {
    N1qlQuery q = N1qlQuery.simple(
      select("*").from("`" + DB + "`")
        .where(
          (x(TYPE).eq(s(RECOMMENDATION)))
            .and(x("`" + USER + "`.`" + ID + "`").eq(s(user.getId())))
        )
    );
    List<N1qlQueryRow> rows = bucket.query(q).allRows();
    return rows.stream()
      .map(r -> new Recommendation(r.value().getObject(DB))).collect(Collectors.toList());
  }

  /** Get recommendations by episodeId **/
  public List<Recommendation> getRecommendations(String episodeId, Integer offset, Integer max) {
    N1qlQuery q = N1qlQuery.simple(
      select("*").from("`" + DB + "`")
      .where(
        (x(TYPE).eq(s(RECOMMENDATION)))
        .and(x("`" + EPISODE_ID + "`").eq(s(episodeId)))
      ).limit(max).offset(offset)
    );
    List<N1qlQueryRow> rows = bucket.query(q).allRows();
    return rows.stream()
      .map(r -> new Recommendation(r.value().getObject(DB))).collect(Collectors.toList());
  }

  /** Get episode-recommendation boolean mappings */
  public HashMap<String, Boolean> getEpsiodeRecommendationMappings(String userId, List<String> episodeIds) {
    List<String> keys = episodeIds.stream().map(id -> Recommendation.composeKey(id, userId)).collect(Collectors.toList());
    List<JsonDocument> foundDocs = Observable.from(keys)
      .flatMap(key -> Observable.just(bucket.get(key)))
      .toList()
      .toBlocking()
      .single();
    List<Recommendation> recommendations = foundDocs.stream()
      .filter(doc -> doc != null)
      .map(doc -> new Recommendation(doc.content()))
      .collect(Collectors.toList());
    HashMap<String, Boolean> result = new HashMap<String, Boolean>();
    for (Recommendation recommendation : recommendations) {
      result.put(recommendation.getEpisode().getId(), true);
    }
    for (String eId : episodeIds) {
      if (!result.containsKey(eId)) result.put(eId, false);
    }
    return result;
  }

}
