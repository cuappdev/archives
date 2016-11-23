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
      if @followed_user.remote_push_notifications_enabled) 
          notify(@folowed_user.push_id) 
      end 
    end
    render json: { success: success_val, follow: true }
  end

  def notify(user_push_id)
    url = "http://9144f8af.ngrok.io/push" #TODO
    headers = {'Content-Type' =>'application/json'}
    body = {:app => "TEMPO",
            :message =>  "Someone is following you!", #TODO
            :target_ids => [user_push_id],
            :notification => 2}
    res = post_no_ssl(headers, body.to_json, url)
  end

  def destroy
    followed_id = params[:followed_id]
    success_val = @user.unfollow(followed_id)
    render json: { success: success_val, follow: false}
  end
end
