package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._

trait Protocol extends StockProtocol {


  // Episode formatting
  implicit val episodeFormat =
    new EntityProtocol[EpisodeFields, EpisodeEntity](jsonFormat6(EpisodeFields), EpisodeFactory.instantiate)

  // User formatting
  implicit val userFormat =
    new EntityProtocol[UserFields, UserEntity](jsonFormat1(UserFields), UserFactory.instantiate)

  implicit val likeFormat =
    new EntityProtocol[LikeFields, LikeEntity](jsonFormat2(LikeFields), LikeFactory.instantiate)

  implicit val seriesFormat =
    new EntityProtocol[SeriesFields, SeriesEntity](jsonFormat4(SeriesFields), SeriesFactory.instantiate)

  implicit val subscriptionFormat =
    new EntityProtocol[SubscriptionFields, SubscriptionEntity](jsonFormat2(SubscriptionFields), SubscriptionFactory.instantiate)


}
