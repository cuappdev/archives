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
  before_action :authorize, only: [:create, :destroy]
  include HttpHelper
  def create
    followed_id = (params[:followed_id])
    # cant follow yourself
    if @user.id == followed_id
      render json: { success: false, follow: follow_bool}
    end
    # success value on the follow or unfollow
    success_val = @user.follow(followed_id)
    if success_val 
      @followed_user = User.find(followed_id)
      if shouldNotify(@user, @followed_user) 
          msg = "@#{@user.username} is following you!"
          Notification.create(from: @user.id, to: followed_id, notification_type: 2, message: msg)
          Notification.notify([@followed_user.push_id], msg, 2) 
      end 
    end
    render json: { success: success_val, follow: true }
  end

  def shouldNotify(user, followed_user) # user is trying to follow followed_user
    return (!followed_user.push_id.nil? and 
           followed_user.remote_push_notifications_enabled and 
           !Notification.exists?(from:user.id, to:followed_user.id, notification_type:2))
  end 

  def destroy
    followed_id = params[:followed_id]
    success_val = @user.unfollow(followed_id)
    render json: { success: success_val, follow: false}
  end
end
