from marshmallow_sqlalchemy import ModelSchema
from app.podcastml.models.series_for_topic import *

class SeriesForTopicSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SeriesForTopic
