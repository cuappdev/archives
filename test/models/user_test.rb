# == Schema Information
#
# Table name: users
#
#  id              :integer          not null, primary key
#  name            :string
#  hipster_score   :integer
#  caption         :string
#  location_id     :integer
#  created_at      :datetime         not null
#  updated_at      :datetime         not null
#  followers_count :integer          default(0)
#  like_count      :integer          default(0)
#  fbid            :string
#  username        :string
#

require 'test_helper'

class UserTest < ActiveSupport::TestCase
  test "should follow and unfollow a user" do
    ilan = User.create(username: 'Tennismaster982', fname: 'Ilan', lname: 'Filonenko', hipster_score: 1)
    feifan = User.create(username: 'feifanzhou', fname: 'Feifan', lname: 'Zhou', hipster_score: 1)
    assert_not ilan.following?(feifan)
    assert feifan.followers_count==0
    ilan.follow(feifan)
    assert feifan.followers_count==1
    assert ilan.following?(feifan)
    ilan.unfollow(feifan)
    assert feifan.followers_count==0
    assert_not ilan.following?(feifan)
  end
  test "should be able to like" do
    ilan = User.create(username: 'Tennismaster982', fname: 'Ilan', lname: 'Filonenko', hipster_score: 1)
    assert ilan.like_count==0
    post = Post.create(user_id: 1)
    assert post.like_count==0
    ilan.like(post)
    assert post.like_count==1
    assert ilan.like_count==1
  end
  test "should songs be connected to posts" do
    song = Song.create(spotify_url: "facebook.com", artist: "Red Hot Chilli Peppers", track: "Cant Stop")
    post = Post.create(user_id: 1)
    songpost = SongPost.create(post_id: post.id, song_id: song.id)
    assert song.posts.count()==1
    assert post.songs.count()==1

  end
end
