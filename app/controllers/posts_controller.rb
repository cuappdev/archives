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
    if (Song.exists?(spotify_url: params[:song][:spotify_url]))
      @song = Song.find_by(spotify_url: params[:song][:spotify_url])
      hipster_user = User.find(@song.posts.sort_by { |hsh| hsh[:created_at] }[0].user_id)
    else
      @song = Song.create(song_params)
    end
    @song_post = SongPost.create(post_id: @post.id, song_id: @song.id)
    @success = (!@song.id.blank? and !@post.id.blank? and @post.songs.count==1)
    if @success
      time_from = @song_post.created_at
      hipster_count = 4 - (Post.where(user_id: user_id, created_at: (time_from - 24.hours)..time_from).count)
      @user.increment(:hipster_score, hipster_count).save 
    end
    hipster_user.increment(:hipster_score, 10).save if (!hipster_user.blank? and @success)
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
          playlist = @spotify_cred.playlist_id
          username = @spotify_cred.spotify_id
          uri = URI.parse("https://api.spotify.com/v1/users/#{username}/playlists/#{playlist}/tracks?uris=#{url}")
          http = Net::HTTP.new(uri.host, uri.port)
          http.use_ssl = true
          http.verify_mode = OpenSSL::SSL::VERIFY_NONE
          request = Net::HTTP::Post.new(uri.request_uri, {'Accept' =>'application/json', "Authorization" => access_token})
          response = http.request(request)
        end
      end
    end
    true
  end
end
