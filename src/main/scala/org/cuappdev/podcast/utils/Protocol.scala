package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._

trait Protocol extends StockProtocol {

  // Formatting for entities

  implicit val episodeFormat =
    new EntityProtocol[EpisodeFields, EpisodeEntity](jsonFormat6(EpisodeFields), EpisodeFactory.instantiate)

  implicit val userFormat =
    new EntityProtocol[UserFields, UserEntity](jsonFormat1(UserFields), UserFactory.instantiate)

  implicit val likeFormat =
    new EntityProtocol[LikeFields, LikeEntity](jsonFormat2(LikeFields), LikeFactory.instantiate)

  implicit val seriesFormat =
    new EntityProtocol[SeriesFields, SeriesEntity](jsonFormat4(SeriesFields), SeriesFactory.instantiate)

  implicit val subscriptionFormat =
    new EntityProtocol[SubscriptionFields, SubscriptionEntity](jsonFormat2(SubscriptionFields), SubscriptionFactory.instantiate)


  // Formatting for fields

  implicit val episodeFieldsFormat =
    new FieldsProtocol[EpisodeFields](jsonFormat6(EpisodeFields))

  implicit val userFieldsFormat =
    new FieldsProtocol[UserFields](jsonFormat1(UserFields))

  implicit val likeFieldsFormat =
    new FieldsProtocol[LikeFields](jsonFormat2(LikeFields))

  implicit val seriesFieldsFormat =
    new FieldsProtocol[SeriesFields](jsonFormat4(SeriesFields))

  implicit val subscriptionFieldsFormat =
    new FieldsProtocol[SubscriptionFields](jsonFormat2(SubscriptionFields))


}

object Protocol extends Protocol
