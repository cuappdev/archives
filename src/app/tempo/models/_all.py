from app.tempo.models.following import *
from app.tempo.models.like import *
from app.tempo.models.notification import *
from app.tempo.models.post import *
from app.tempo.models.session import *
from app.tempo.models.song_post import *
from app.tempo.models.song import *
from app.tempo.models.spotify_cred import *
from app.tempo.models.user import *

class FollowingSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Following

class LikeSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Like

class NotificationSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Notification

class PostSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Post
  song_posts = fields.Nested('SongPostSchema', many=True)
  likes = fields.Nested('LikeSchema', many=True)
  user = fields.Nested('UserSchema', many=False)

class SessionSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Session

class SongPostSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SongPost
  song = fields.Nested('SongSchema', many=False)

class SongSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Song

class SpotifyCredSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SpotifyCred

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User
