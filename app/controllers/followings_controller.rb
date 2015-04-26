class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    @unfollow = params[:unfollow]
    if @unfollow
      @user.unfollow(follow_params[:follower_id])
      @success = true
    else
      @user.follow(follow_params[:follower_id])
      @success = true
    end
    render json: { success: @success, follow: !@unfollow }
  end

  private
  def follow_params
    params.require(:follower_id, :unfollow)
  end
end
