# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  views      :integer
#

require_relative '../rails_helper'

RSpec.describe PostsController, type: :controller do

  before(:each) do
    @s = FactoryGirl.create(:song, spotify_url: "http://example.com/foo")
  end

  it "creates song post given song data" do
    post :create, song: {:spotify_url => "http://example.com/foo"}
    response_json = check_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["post"]).to_not eq({}) # Post should be non-empty
  end

  it "doesn't create song for nonexistent song data" do
    post :create, song: {:spotify_url => "http://example.com/bar"}
    response_json = check_response(response)
    expect(response_json["success"]).to eq(false)
  end
end
