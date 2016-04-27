# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  username   :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  like_count :integer          default(0)
#  user_id    :integer
#

class PostsController < ApplicationController
  before_action :authorize, only: [:create]
  # Create a SongPost where Song might be already existing
  def create
    user_id = @session.user_id
    @post = Post.create(user_id: user_id)
    @song = Song.exists?(spotify_url: params[:song][:spotify_url]) ? Song.find_by(spotify_url: params[:song][:spotify_url]) : Song.create(song_params)
    SongPost.create(post_id: @post.id, song_id: @song.id)
    @success = (!@song.id.blank? and !@post.id.blank? and @post.songs.count==1)
    User.increment_counter(:hipster_score,@user) if @success
    if (@success)
       add_to_followers_playlist(user_id, params[:song][:spotify_url])
    end
    render json: { success: !@song.blank?, post: @post.as_json(id: user_id) }
  end
  private
  def song_params
    params.require(:song).permit(:artist, :track, :spotify_url)
  end

  def add_to_followers_playlist(user_id, song_url)
    url = "spotify:track:" + song_url
    @user = User.find(user_id)
    if (!@user.followers_ids.blank?)
      @user.followers.each do |follower|
        @spotify_cred = SpotifyCred.find_by_user_id(follower)
        if (@spotify_cred)
          access_token = "Bearer #{@spotify_cred.access_token}"
          p access_token
          playlist = @spotify_cred.playlist_id
          p playlist
          username = @spotify_cred.spotify_id
          uri = URI.parse("https://api.spotify.com/v1/users/#{username}/playlists/#{playlist}/tracks?uris=#{url}")
          p "IN FUNCTION"
          p uri
          http = Net::HTTP.new(uri.host, uri.port)
          p http
          http.use_ssl = true
          http.verify_mode = OpenSSL::SSL::VERIFY_NONE
          request = Net::HTTP::Post.new(uri.request_uri, {'Accept' =>'application/json', "Authorization" => access_token})
          p request
          response = http.request(request)
          p response
        end
      end
    end
    true
  end
end
