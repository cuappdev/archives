require 'rails_helper'
require './helpers'

RSpec.describe FollowingsController, type: :controller do

  before(:each) do
    @user1 = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
    @user2 = FactoryGirl.create(:user, fbid: "fake", username: "alsovalid")
  end

  it "follows previously unfollowed user" do
    post :followings, unfollow: "0", followed_id: @user2.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["follow"]).to eq(true)
  end

  it "unfollows previously followed user" do
    @f = FactoryGirl.create(:following, follower_id: @user1.id, followed_id: @user2.id)
    post :followings, unfollow: "1", followed_id: @user2.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["follow"]).to eq(false)
  end

  it "doesn't unfollow previously unfollowed user" do
    post :followings, unfollow: "1", followed_id: @user2.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

  it "doesn't follow previously followed user" do
    @f = FactoryGirl.create(:following, follower_id: @user1.id, followed_id: @user2.id)
    post :followings, unfollow: "0", followed_id: @user2.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

  it "cannot follow yourself" do
    post :followings, follower_id: @user1.id, followed_id: @user1.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

end
