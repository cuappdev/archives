package org.cuappdev.podcast.utils

import org.cuappdev.podcast.models._

trait Protocol extends StockProtocol {


  // Episode formatting
  implicit val episodeFormat =
    new EntityProtocol[EpisodeFields, EpisodeEntity](jsonFormat6(EpisodeFields), EpisodeFactory.instantiate)

  // User formatting
  implicit val userFormat =
    new EntityProtocol[UserFields, UserEntity](jsonFormat1(UserFields), UserFactory.instantiate)


  // TODO: More models



}
