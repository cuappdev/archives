# == Schema Information
#
# Table name: songs
#
#  id            :integer          not null, primary key
#  spotify_url   :string
#  artist        :string
#  track         :string
#  hipster_score :integer
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#

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

end
