# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

require 'rails_helper'

RSpec.describe Post, type: :model do

  before (:each) do
    @p = FactoryGirl.create(:post, like_count: 0, user_id: 1)
    @s1 = FactoryGirl.create(:song, spotify_url: "http://example.com/1")
    @s2 = FactoryGirl.create(:song, spotify_url: "http://example.com/2")
    @sp1 = FactoryGirl.create(:song_post, post_id: @p.id, song_id: @s1.id)
    @sp2 = FactoryGirl.create(:song_post, post_id: @p.id, song_id: @s2.id)
  end

  it "tests validation of post" do
    expect(@p.valid?).to eq(true)
    @p.like_count = -1
    expect(@p.valid?).to eq(false)
  end

end
