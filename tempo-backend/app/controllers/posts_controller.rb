# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  views      :integer
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
      hipster_count = 5 - (Post.where(user_id: user_id, created_at: (Time.zone.now.beginning_of_day..Time.zone.now.end_of_day)).count)
      offset = [hipster_count, -@user.hipster_score].max
      @user.increment(:hipster_score, offset).save
    end
    hipster_user.increment(:hipster_score, 10).save if (!hipster_user.blank? and @success)
    render json: { success: !@song.blank?, post: @post.as_json(id: user_id) }
  end

  def viewed
      Post.find(params[:id]).increment(:views, 1).save
      render json: { success: true, views: Post.find(params[:id].views) }
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
          token_hash = {
            access_token: @spotify_cred.access_token,
            refresh_token: @spotify_cred.refresh_token,
            expires_at: @spotify_cred.expires_at.to_i
          }
          access_token = OAuth2::AccessToken.from_hash(client, token_hash)
          final_token = access_token.token
          final_expires_at = access_token.expires_at
          if access_token.expired?
            b = Base64.strict_encode64("#{ENV["spotify_client_id"]}:#{ENV["spotify_client_secret"]}")
            response = HTTParty.post(
              "https://accounts.spotify.com/api/token",
              :body => {:grant_type => "refresh_token",
                        :refresh_token => "#{access_token.refresh_token}"},
              :headers => {"Authorization" => "Basic #{b}"}
            )
            json_response = JSON.parse(response.body)
            final_token = json_response["access_token"]
            final_expires_at = (DateTime.now.to_time + json_response["expires_in"]).to_datetime.to_time.to_i
            @spotify_cred.update_attributes(access_token: final_token, expires_at: final_expires_at )
          end
          access_token = "Bearer #{final_token}"
          playlist = @spotify_cred.playlist_id
          username = @spotify_cred.spotify_id
          url = "#{SPOTIFY_URL}users/#{username}/playlists/#{playlist}/tracks?uris=#{url}"
          header = {'Accept' =>'application/json', "Authorization" => access_token}
          response = post(header, {}, url)

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
  def client
    @client ||= OAuth2::Client.new(ENV["spotify_client_id"], ENV["spotify_client_secret"], site: 'https://accounts.spotify.com', token_url: '/api/token')
  end
end