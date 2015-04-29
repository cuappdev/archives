class PostsController < ApplicationController
  before_action :authorize, only: [:create]
  def create
    user_id = @session.user_id
    @post = Post.create(user_id: user_id, like_count: 0)
    @song = Song.create(spotify_url: params[:spotify_url])
    SongPost.create(post_id: post.id, song_id: song.id)
    @success = (!@song.id.blank? and !@post.id.blank? and @post.songs.count==1)
    render json: { success: !@song.blank?, post: @post }
  end
end
