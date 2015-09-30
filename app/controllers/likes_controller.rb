class LikesController < ApplicationController
  before_action :authorize, only: [:create, :is_liked]
  def create
    unlike = params[:unlike]
    post_id = params[:post_id]
    post = Post.find(post_id) unless post_id.blank?
    if post.blank?
      render json: {success: false, liked: !@unlike}
    end
    success_val = (unlike == "1" ? @user.unlike(post_id) : @user.like(post_id))
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
