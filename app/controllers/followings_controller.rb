class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    unfollow = params[:unfollow]
    followed_id = params[:followed_id]
    unfollow || unfollow == 1 ? @user.unfollow(followed_id) : @user.follow(followed_id)
    render json: { success: true, follow: !unfollow }
  end

end
