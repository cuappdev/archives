class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]
  include FollowingsHelper
  def create
    follow_bool = (params[:unfollow] == "0")
    p 'are you following? '
    p follow_bool
    followed_id = params[:followed_id]
    if @user.id == followed_id
      render json: { success: false, follow: follow_bool}
    end
    success_val = (follow_bool ? @user.follow(followed_id) : @user.unfollow(followed_id))
    update_mutual_friends(follow_bool, @user, followed_id) if success_val
    render json: { success: success_val, follow: follow_bool }
  end
end
