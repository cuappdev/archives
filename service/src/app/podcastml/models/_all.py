from marshmallow_sqlalchemy import ModelSchema
from app.podcastml.models.series_for_topic import *
from app.podcastml.models.series_for_user import *
from app.podcastml.models.episodes_for_topic import *
from app.podcastml.models.episodes_for_user import *

class SeriesForTopicSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SeriesForTopic

class SeriesForUserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SeriesForUser

class EpisodesForTopicSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = EpisodesForTopic

class EpisodesForUserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = EpisodesForUser
