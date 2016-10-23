require 'rails_helper'

RSpec.describe Song, type: :model do

  before (:each) do
    @u = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
    @p = FactoryGirl.create(:post, like_count: 0, user_id: @u.id)
    @s = FactoryGirl.create(:song, spotify_url: "http://example.com/1")
    @sp = FactoryGirl.create(:song_post, post_id: @p.id, song_id: @s.id)
  end

  it "tests validation of song" do
    expect(@s.valid?).to eq(true)
    @p.like_count = -1
    expect(@p.valid?).to eq(false)
  end

  it "tests posts of song" do
    expect(@s.posts.length).to eq(1)
  end

  it "tests number of users of song" do
    expect(@s.number_of_users).to eq(1)
  end

end
