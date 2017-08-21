from following import *
from like import *
from notification import *
from post import *
from session import *
from song_post import *
from song import *
from spotify_cred import *
from user import *

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

class SessionSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Session

class SongPostSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SongPost

class SongSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Song

class SpotifyCredSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = SpotifyCred

class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User
