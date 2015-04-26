class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    @follow = Following.find_by(follower_id: @user.id, followed_id: params[:following][:followed_id])
    @unfollow = params[:following][:dislike]
    if @follow && @unfollow
      @user.unfollow(User.find_by(params[:following][:followers_id]))
      @message = true
    elsif @follow && !@unfollow
      @message = false
    else
      @follow = Follow.create(follow_params)
      @user.following(User.find_by(params[:following][:followers_id]))
      @message = true
    end
    render json: { message: @message, follow: @follow }
  end

  private
  def follow_params
    params.require(:following).permit(:follower_id, :unfollow)
  end
end
