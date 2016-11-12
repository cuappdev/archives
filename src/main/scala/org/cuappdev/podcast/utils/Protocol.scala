package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._

trait Protocol extends StockProtocol {

  // Formatting for fields

  implicit val episodeFieldsFormat = jsonFormat6(EpisodeFields)

  implicit val userFieldsFormat = jsonFormat1(UserFields)

  implicit val likeFieldsFormat = jsonFormat2(LikeFields)

  implicit val seriesFieldsFormat = jsonFormat4(SeriesFields)

  implicit val subscriptionFieldsFormat = jsonFormat2(SubscriptionFields)

  // Formatting for entities

  implicit val episodeFormat =
    new EntityProtocol[EpisodeFields, EpisodeEntity](episodeFieldsFormat, EpisodeFactory.instantiate)

  implicit val userFormat =
    new EntityProtocol[UserFields, UserEntity](userFieldsFormat, UserFactory.instantiate)

  implicit val likeFormat =
    new EntityProtocol[LikeFields, LikeEntity](likeFieldsFormat, LikeFactory.instantiate)

  implicit val seriesFormat =
    new EntityProtocol[SeriesFields, SeriesEntity](seriesFieldsFormat, SeriesFactory.instantiate)

  implicit val subscriptionFormat =
    new EntityProtocol[SubscriptionFields, SubscriptionEntity](subscriptionFieldsFormat, SubscriptionFactory.instantiate)


}

object Protocol extends Protocol
