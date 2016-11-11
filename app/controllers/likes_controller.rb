# == Schema Information
#
# Table name: likes
#
#  id         :integer          not null, primary key
#  post_id    :integer
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#
require 'json'
class LikesController < ApplicationController
  include HttpHelper
  before_action :authorize, only: [:create, :is_liked]
  def create
    @unlike = params[:unlike]
    post_id = params[:post_id]
    post = Post.find(post_id) unless post_id.blank?
    if (post.blank? or post_id.blank?)
      render json: {success: false, liked: !@unlike}
    end
    success_val = @user.like(post_id)
    if success_val
        @user = User.find(post.user_id)
        @user.increment(:hipster_score, 1).save
        notify(@user.push_id) 
    end
    render json: { success: success_val, liked: true }
  end

  def notify(user_push_id)
    url = "http://10.145.5.191:8080/push" #TODO
    headers = {'Content-Type' =>'application/json'} 
    body = {:app => "TEMPO", 
            :message =>  "Someone liked your post!", 
            :target_ids => [user_push_id],  
            :notification => 1}
    res = post_no_ssl(headers, body.to_json, url)
  end 

  def destroy
    post_id = params[:post_id]
    success_val = @user.unlike(post_id)
    if success_val
      User.find(post.user_id).increment(:hipster_score, -1).save
    end
    render json: { success: success_val, liked: false }
  end

  def is_liked
    post_id = params[:params]
    post = Post.find(post_id) unless post_id.blank?
    if post.blank?
      render json: {success: false}
    end
    render json: {success: true, liked: @user.liked?(post_id)}
  end
end
