class FeedController < ApplicationController
  before_action :authorize, only: [:index]
  def index
    followings_ids = @user.followings_ids
    posts = Post
      .where(created_at: (Time.now - 24.hours)..Time.now)
      .where('user_id IN (?)', followings_ids + [@user.id])
      .order('created_at DESC')
      .map { |post| post.as_json(id: @user.id) }
    render json: { posts: posts }
  end
end