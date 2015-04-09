class PostsController < ApplicationController
  before_action :authorize, only: [:create]
  def create
    user_id = @session.user_id
    @post = Post.create(user_id: user_id)
    @song = Song.create(params[:song])
    render json: { success: !@song.blank?, post: @post }
  end
end
