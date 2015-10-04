class FeedController < ApplicationController
  before_action :authorize, only: [:index]
  def index
    followings_ids = @user.followings_ids
    posts = Post
      .where('created_at >= ?', Time.now.midnight)
      .where('user_id IN (?)', followings_ids)
      .order('created_at DESC')
      .map { |post| post.as_json(id: @user.id)  }
    render json: { posts: posts }
  end
end