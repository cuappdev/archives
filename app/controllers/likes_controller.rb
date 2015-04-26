class LikesController < ApplicationController
  def create
    @like = Like.find_by(post_id: params[:like][:post_id])
    if @like
      @message = false
    else
      @like = Like.create(like_params)
      User.find_by(id: params[:like][:user_id]).like(Post.find_by(id: params[:like][:post_id]))
      @message = true
    end
    render json: { message: @message, like: @like }
  end

  private
  def like_params
    params.require(:like).permit(:user_id, :post_id)
  end
end
