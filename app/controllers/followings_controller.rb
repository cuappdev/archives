class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]
  include FollowingsHelper
  def create
    # Is following?
    follow_bool = (params[:unfollow] == "0")
    # following id
    followed_id = params[:followed_id]
    # cant follow yourself
    if @user.id == followed_id
      render json: { success: false, follow: follow_bool}
    end
    # success value on the follow or unfollow
    success_val = (follow_bool ? @user.follow(followed_id) : @user.unfollow(followed_id))
    # if successful update the mutual friends by passing in whether it was follow, 
    # the user who followed, and the follower
    update_mutual_friends(follow_bool, @user, followed_id) if success_val
    render json: { success: success_val, follow: follow_bool }
  end
end
