class FeedController < ApplicationController
  before_action :authorize
  def index
    following_ids = @user.following.pluck(:id)
    following_ids = [following_ids] unless following_ids.is_a? Array
    render json: { posts: Post.where('created_at >= ?', Time.now.midnight).where('user_id in ?', following_ids).order('created_at DESC') }
  end
end
