require 'rails_helper'
require_relative 'helpers'

RSpec.describe LikesController, type: :controller do

  before(:each) do
    @u = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
    @p = FactoryGirl.create(user_id: @u.id)
  end

  it "likes previously not-liked post" do
    post :likes, unlike: "0", post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["liked"]).to eq(true)
  end

  it "unlikes previously liked post" do
    l = FactoryGirl.create(:like, user_id: @u.id, post_id: @p.id)
    post :likes, unlike: "1", post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["liked"]).to eq(false)
  end

  it "doesn't like previously not-liked post" do
    post :likes, unlike: "1", post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

  it "doesn't like previously liked post" do
    l = FactoryGirl.create(:like, user_id: @u.id, post_id: @p.id)
    post :followings, unlike: "0", post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

  it "is_like fails for nonexistent post" do
    get :is_liked, post_id: 9e99
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(false)
  end

  it "is_like true when user has liked post" do
    l = FactoryGirl.create(:like, user_id: @u.id, post_id: @p.id)
    get :is_liked, post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["liked"]).to eq(true)
  end

  it "is_like false when user has not liked post" do
    get :is_liked, post_id: @p.id
    response_json = extract_response(response)
    expect(response_json["success"]).to eq(true)
    expect(response_json["liked"]).to eq(false)
  end
end
