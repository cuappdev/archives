class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    @follow = Following.find_by(follower_id: @user.id, followed_id: params[:following][:followed_id])
    @unfollow = params[:following][:unfollow]
    if @follow && @unfollow
      @user.unfollow(follow_params[:follower_id])
      @message = true
    elsif @follow && !@unfollow
      @message = false
    else
      @user.follow(follow_params[:follower_id])
      @message = true
    end
    render json: { message: @message, follow: @follow }
  end

  private
  def follow_params
    params.require(:following).permit(:follower_id, :unfollow)
  end
end
