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
    #if (@success)
    #    add_to_followers_playlist(user_id, params[:song][:spotify_url])
    #end
    render json: { success: !@song.blank?, post: @post.as_json(id: user_id) }
  end
  private
  def song_params
    params.require(:song).permit(:artist, :track, :spotify_url)
  end

  def add_to_followers_playlist(user_id, song_url)
      data = {:uris => song_url}
      @user = User.find_by(:id, user_id)
      followers = @user.followers
      p "IN FUNCTION WOOT WOOT"
      p followers
      if (followers)
         followers.each do |follower|
            @spotify_cred = SpotifyCred.find_by(:user_id, follower)
            if (@spotify_cred)
                data = {:uris => song_url}
                access_token = @spotify_cred.access_token
                playlist = @spotify_cred.playlist_id
                user = @spotify_cred.spotify_id
                uri = URI.parse('https://api.spotify.com/v1/users/'+ user + '/playlists/' + playlist + "/tracks")
                http = Net::HTTP.new(uri.host, uri.port)
                http.use_ssl = true
                http.verify_mode = OpenSSL::SSL::VERIFY_NONE
                request = Net::HTTP::POST.new(uri.request_uri, {'Content-Type' =>'application/json', Authorization => access_token})
                request.body = data.to_json
                response = http.request(request)
            end
         end
      end
  end
end
