class PostsController < ApplicationController
  before_action :authorize, only: [:create]
  def create
    user_id = @session.user_id
    @post = Post.create(user_id: user_id)
    @song = Song.create(params[:song])
    SongPost.create(post_id: post.id, song_id: song.id)
    @success = (!@song.blank? and @post.songs.count==1) ? true : false
    render json: { success: !@song.blank?, post: @post, song: @song }
  end
end
