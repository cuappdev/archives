require 'rails_helper'

RSpec.describe SongPost, type: :model do

  before (:each) do
    @p = FactoryGirl.create(:post, like_count: 0, user_id: 1)
    @s = FactoryGirl.create(:song, spotify_url: "http://example.com/1")
    @sp = FactoryGirl.create(:song_post, post_id: @p.id, song_id: @s.id)
  end

  it "validates song post" do
    expect(@sp.valid?).to eq(true)
  end

end
