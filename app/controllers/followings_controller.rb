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
      if @followed_user.remote_push_notifications_enabled 
          notify(@followed_user.push_id, @user.username) 
      end 
    end
    render json: { success: success_val, follow: true }
  end

  def notify(followed_push_id, follower_username)
    url = "http://35.162.35.23/push"
    headers = {'Content-Type' =>'application/json'}
    body = {:app => "TEMPO",
            :message =>  "#{follower_username} is following you!", 
            :target_ids => [followed_push_id],
            :notification => 2}
    res = post_no_ssl(headers, body.to_json, url)
  end

  def destroy
    followed_id = params[:followed_id]
    success_val = @user.unfollow(followed_id)
    render json: { success: success_val, follow: false}
  end
end
