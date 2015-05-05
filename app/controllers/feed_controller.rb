class FeedController < ApplicationController
  before_action :authorize
  def index
    render json: { posts: Post.where('created_at >= ?', Time.now.midnight).where('user_id in ?', @user.following.pluck(:id)).order('created_at DESC') }
  end
end
