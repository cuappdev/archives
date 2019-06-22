package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._

trait Protocol extends BaseProtocol {


  implicit val episodeFieldsFormat = jsonFormat6(EpisodeFields)
  implicit val episodeFormat =
    new EntityProtocol[EpisodeFields, EpisodeEntity](episodeFieldsFormat, EpisodeFactory.instantiate)


  implicit val userFieldsFormat = jsonFormat1(UserFields)
  implicit val userFormat =
    new EntityProtocol[UserFields, UserEntity](userFieldsFormat, UserFactory.instantiate)


  implicit val likeFieldsFormat = jsonFormat2(LikeFields)
  implicit val likeFormat =
    new EntityProtocol[LikeFields, LikeEntity](likeFieldsFormat, LikeFactory.instantiate)


  implicit val seriesFieldsFormat = jsonFormat4(SeriesFields)
  implicit val seriesFormat =
    new EntityProtocol[SeriesFields, SeriesEntity](seriesFieldsFormat, SeriesFactory.instantiate)


  implicit val subscriptionFieldsFormat = jsonFormat2(SubscriptionFields)
  implicit val subscriptionFormat =
    new EntityProtocol[SubscriptionFields, SubscriptionEntity](subscriptionFieldsFormat, SubscriptionFactory.instantiate)


  implicit val sessionFieldsFormat = jsonFormat4(SessionFields)
  implicit val sessionFormat =
    new EntityProtocol[SessionFields, SessionEntity](sessionFieldsFormat, SessionFactory.instantiate)


}

object Protocol extends Protocol
