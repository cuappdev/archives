# == Schema Information
#
# Table name: followings
#
#  id          :integer          not null, primary key
#  follower_id :integer
#  followed_id :integer
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]
  include FollowingsHelper
  def create
    followed_id = (params[:followed_id])
    # cant follow yourself
    if @user.id == followed_id
      render json: { success: false, follow: follow_bool}
    end
    # success value on the follow or unfollow
    success_val = @user.follow(followed_id)
    render json: { success: success_val, follow: true }
  end

  def destroy
    success_val = @user.unfollow(followed_id)
    render json: { success: success_val, follow: false}
  end
end
