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
  before_action :authorize, only: [:create, :is_liked, :destroy]
  def create
    post_id = params[:post_id]
    db_post = Post.find(post_id) unless post_id.blank?
    if (db_post.blank? or post_id.blank?)
      render json: {success: false, liked: !@unlike}
    end
    success_val = @user.like(db_post)
    if success_val
        @poster = User.find(db_post.user_id)
        @poster.increment(:hipster_score, 1).save
        track_name = db_post.songs.first.track
        if shouldNotify(@user, @poster, post_id)
          msg = "@#{@user.username} liked a song you posted: #{track_name}!"
          Notification.create(from: @user.id, to: @poster.id, post_id: post_id, notification_type: 1, message: msg)
          notify([@poster.push_id], msg, 1) 
        end 
    end
    render json: { success: success_val, liked: true }
  end

  def shouldNotify(user, poster, post_id) # user likes post (w/ post_id) of poster
    return (poster.id != user.id and 
           !poster.push_id.nil? and 
           poster.remote_push_notifications_enabled and
           !Notification.exists?(from: user.id, post_id: post_id, notification_type: 1)) 
  end 

  def destroy
    post_id = params[:post_id]
    @post = Post.find(post_id)
    success_val = @user.unlike(post_id)
    if success_val
      poster = User.find(@post.user_id)
      if poster.hipster_score != 0
        poster.increment(:hipster_score, -1).save
      end
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
