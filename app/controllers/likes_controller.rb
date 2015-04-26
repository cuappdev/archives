class LikesController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    @like = Like.find_by(post_id: params[:like][:post_id])
    @dislike = params[:like][:dislike]
    if @like && @dislike
      @user.dislike(Post.find_by(id: params[:like][:post_id]))
      @message = true
    elsif @like && !@dislike
      @message = false
    else
      @like = Like.create(like_params)
      @user.like(Post.find_by(id: params[:like][:post_id]))
      @message = true
    end
    render json: { message: @message, like: @like }
  end

  private
  def like_params
    params.require(:like).permit(:post_id, :dislike)
  end
end
