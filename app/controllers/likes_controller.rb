class LikesController < ApplicationController
  before_action :authorize, only: [:create]

  def create
    @dislike = params[:dislike]
    if @dislike
      @user.unlike(Post.find(params[:post_id]))
      @success = true
    else
      @user.like(Post.find(params[:post_id]))
      @success = true
    end
    render json: { success: @success, liked: !@dislike }
  end

  private
  def like_params
    params.require(:post_id, :dislike)
  end
end
