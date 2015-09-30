class FeedController < ApplicationController
  before_action :authorize
  def index
    following_ids = @user.followings_ids
    # render json: { posts: Post.where('created_at >= ?', Time.now.midnight).where('user_id in ?', following_ids).order('created_at DESC') }
    render json: { posts: Post.where('created_at >= ?', Time.now.midnight).where('user_id IN (?)', followings_ids).order('created_at DESC') }
  end
end