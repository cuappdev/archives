# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

u = User.create(name: 'Ilan', username: 'Allan', fbid: '4', hipster_score: 9001)
s = Session.create(user_id: u.id)
post = Post.create(user_id: u.id, username: u.username)
post2 = Post.create(user_id: u.id, username: u.username)
song = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Queen', track: 'Bohmeian Rhapsody')
song2 = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Lady Gaga', track: 'Bad Romance')
SongPost.create(post_id: post.id, song_id: song.id)
SongPost.create(post_id: post2.id, song_id: song2.id)

