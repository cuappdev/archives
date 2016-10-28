require 'rails_helper'
require './helpers'

RSpec.describe FeedController, type: :controller do

  before(:each) do
    @user1 = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
    @user2 = FactoryGirl.create(:user, fbid: "fake", username: "alsovalid")
    @user3 = FactoryGirl.create(:user, fbid: "something", username: "test")
    @post = FactoryGirl.create(:post, like_count: 0, user_id: @user2.id)
    @f = FactoryGirl.create(:following, follower_id: @user1.id, followed_id: @user2.id)
  end

  it "grabs empty feed properly" do
    # Grab feed when authenticated as @user3
    get :feed
    response_json = extract_response(response)
    expect(response_json["posts"]).to eq([])
  end

  it "grabs feed items properly" do
    # Grab feed when authenticated as user1, who is following user2
    get :feed
    r = { response: response, print: true, success: true }
    response_json = extract_response(response)
    expect(response_json["posts"]).to eq([@post.as_json(id: @user1.id)])
  end

end
