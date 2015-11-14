class PostsController < ApplicationController
  before_action :authorize, only: [:create]
  def create
    user_id = @session.user_id
    @post = Post.create(user_id: user_id, like_count: 0)
    @song = Song.exists?(spotify_url: params[:song][:spotify_url]) ? Song.find_by(spotify_url: params[:song][:spotify_url]) : Song.create(song_params)
    SongPost.create(post_id: @post.id, song_id: @song.id)
    @success = (!@song.id.blank? and !@post.id.blank? and @post.songs.count==1)
    render json: { success: !@song.blank?, post: @post.as_json(id: user_id) }
  end

  private 
  def song_params
    params.require(:song).permit(:artist, :track, :spotify_url)
  end
end
