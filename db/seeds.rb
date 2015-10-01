# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

u = User.create(name: 'Ilan', username: 'Allan', fbid: '4')
s = Session.create(user_id: u.id)
u2 = User.create(name: 'Bob', username: 'Bobby', fbid: '5')
s2 = Session.create(user_id: u2.id)
u3 = User.create(name: 'Feifan', username: 'Feifdom', fbid: '6')
s3 = Session.create(user_id: u3.id)
post = Post.create(user_id: u.id, username: u.username)
post2 = Post.create(user_id: u.id, username: u.username)
song = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Queen', track: 'Bohmeian Rhapsody')
song2 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Lady Gaga', track: 'Bad Romance')
SongPost.create(post_id: post.id, song_id: song.id)
SongPost.create(post_id: post2.id, song_id: song2.id)
post3 = Post.create(user_id: u.id, username: u.username)
post4 = Post.create(user_id: u.id, username: u.username)
song3 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Eminem', track: 'Sayin Goodbye to Holleywood ')
song4 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'RHCP', track: 'Dani California')
SongPost.create(post_id: post3.id, song_id: song3.id)
SongPost.create(post_id: post4.id, song_id: song4.id)
post5 = Post.create(user_id: u.id, username: u.username)
post6 = Post.create(user_id: u.id, username: u.username)
song5 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Martin Garrix', track: 'Animals')
song6 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Martin Garrix', track: 'Wizard')
SongPost.create(post_id: post5.id, song_id: song5.id)
SongPost.create(post_id: post6.id, song_id: song6.id)
post7 = Post.create(user_id: u.id, username: u.username)
post8 = Post.create(user_id: u.id, username: u.username)
song7 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Martin Garrix', track: 'Tremor')
song8 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Martin Garrix', track: 'EDM Bullshit')
SongPost.create(post_id: post7.id, song_id: song7.id)
SongPost.create(post_id: post8.id, song_id: song8.id)

