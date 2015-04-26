class LikesController < ApplicationController
  def create
    @like = Like.find_by(post_id: params[:like][:post_id])
    if @like
      # FIXME: Don't need to create a new session every time, update existing if possible
      @message = 'Already liked'
    else
      @like = Like.create(like_params)
      @message = 'Liked'
    end
    render json: { message: @message, like: @like }
  end

  private
  def like_params
    params.require(:like).permit(:user_id, :post_id)
  end
end
