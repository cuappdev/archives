class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    unfollow = params[:unfollow]
    follower_id = params[:follower_id]
    unfollow ? @user.unfollow(follower_id) : @user.follow(follower_id)
    render json: { success: true, follow: !unfollow }
  end

end
