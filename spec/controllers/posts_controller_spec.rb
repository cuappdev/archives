require 'rails_helper'
require './helpers'

RSpec.describe PostsController, type: :controller do

  before(:each) do
    @s = FactoryGirl.create(:song, spotify_url: "http://example.com/foo")
  end

  it "creates song post given song data" do
    post :posts, song: {:spotify_url => "http://example.com/foo"}
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["post"]).to_not eq({}) # Post should be non-empty
  end

  it "doesn't create song for nonexistent song data" do
    post :posts, song: {:spotify_url => "http://example.com/bar"}
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end
end
