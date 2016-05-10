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

class LikesController < ApplicationController
  before_action :authorize, only: [:create, :is_liked]
  def create
    @unlike = params[:unlike]
    post_id = params[:post_id]
    post = Post.find(post_id) unless post_id.blank?
    if post.blank?
      render json: {success: false, liked: !@unlike}
    end
    success_val = (@unlike == "1" ? @user.unlike(post_id) : @user.like(post_id))
    if success_val
      if @unlike
        User.find(post.user_id).increment(:hipster_score, -1).save
      else
        User.find(post.user_id).increment(:hipster_score, 1).save
      end
    end
    render json: { success: success_val, liked: !@unlike }
  end
  def is_liked
    post_id = params[:post_id]
    post = Post.find(post_id) unless post_id.blank?
    if post.blank?
      render json: {success: false}
    end
    render json: {success: true, liked: @user.liked?(post_id)}
  end
end
