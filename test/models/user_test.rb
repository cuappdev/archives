# == Schema Information
#
# Table name: users
#
#  id               :integer          not null, primary key
#  name             :string
#  hipster_score    :integer
#  caption          :string
#  location_id      :integer
#  created_at       :datetime         not null
#  updated_at       :datetime         not null
#  followers_count  :integer          default(0)
#  like_count       :integer          default(0)
#  fbid             :string
#  username         :string
#  email            :string
#  followings_count :integer          default(0)
#

require_relative '../test_helper'

class UserTest < ActiveSupport::TestCase
  test "should follow and unfollow a user" do
    ilan = User.create(username: 'tennismaster982', name: 'Ilan Filonenko', fbid: '4')
    feifan = User.create(username: 'feifanzhou', name: 'Feifan Zhuo', fbid: '5')
    assert ilan.valid?
    assert feifan.valid?
    assert_not ilan.following?(feifan.id)
    assert ilan.followings_count == 0
    ilan.follow(feifan.id)
    ilan.reload
    feifan.reload
    assert ilan.following?(feifan.id)
    assert ilan.followings_count == 1
    assert feifan.followers_count == 1
    assert_not feifan.following?(ilan.id)
    feifan.follow(ilan.id)
    feifan.reload
    ilan.reload
    assert feifan.following?(ilan.id)
    feifan.followings_count == 1
    ilan.unfollow(feifan.id)
    ilan.reload
    feifan.reload
    assert_not ilan.following?(feifan.id)
    assert feifan.followers_count == 0
    assert ilan.followings_count == 0
  end
  test "should be able to like" do
    ilan = User.create(username: 'tennismaster', name: 'Ilan Filonenko', fbid: '4')
    assert ilan.like_count==0
    post = Post.create(user_id: ilan.id, username: ilan.username)
    assert ilan.valid?
    assert post.valid?
    assert post.like_count == 0
    assert ilan.like_count == 0
    ilan.like(post.id)
    ilan.reload
    post.reload
    assert ilan.liked?(post.id)
    assert ilan.like_count == 1
    assert post.like_count == 1
    ilan.unliked(post.id)
    ilan.reload
    post.reload
    assert ilan.like_count == 0
    assert post.like_count == 0
    assert_not ilan.liked?(post.id)

  end
  test "should songs be connected to posts" do
    ilan = User.create(username: 'tennismaster', name: 'Ilan Filonenko', fbid: '4', hipster_score: 3)
    song = Song.create(spotify_url: 'http://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J', artist: 'Queen', track: 'Bohmeian Rhapsody')
    post = Post.create(user_id: ilan.id, username: ilan.username)
    songpost = SongPost.create(post_id: post.id, song_id: song.id)
    assert song.posts.count()==1
    assert post.songs.count()==1
  end
end
