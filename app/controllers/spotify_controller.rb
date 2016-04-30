require 'net/https'
require 'base64'
class SpotifyController < ApplicationController
  before_action :authorize, only: [:get_access_token]
  def get_hash
    code = params[:code]
    session_code = params[:state]
    token = client.auth_code.get_token(params[:code], redirect_uri: redirect_uri).to_hash
    access_token = "Bearer " + token[:access_token]
    uri = URI.parse('https://api.spotify.com/v1/me')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Get.new(uri.request_uri, {'Content-Type' =>'application/json', 'Authorization' => access_token})
    response = http.request(request)
    res = JSON.parse(response.body)
    username = res["id"]
    @spotify_cred = SpotifyCred.create(user_id: Session.where(code: session_code).limit(1).pluck(:user_id).first,
                                        access_token: token[:access_token],
                                        refresh_token: token[:refresh_token],
                                        expires_at: token[:expires_at],
                                        spotify_id: username)

    data = {:name => "Icefishing Playlist"}
    access_token = "Bearer " + @spotify_cred.access_token
    uri = URI.parse('https://api.spotify.com/v1/users/'+ username + '/playlists')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Post.new(uri.request_uri, {'Content-Type' =>'application/json', "Authorization" => access_token})
    request.body = data.to_json
    response = http.request(request)
    res = JSON.parse(response.body)
    playlistId = res["id"]

    @spotify_cred.update_playlist(playlistId)
    redirect_to "#{ENV["icefishing-app-redirect"]}callback?access_token=#{token[:access_token]}&session_code=#{session_code}&expires_at=#{token[:expires_at]}"
  end
  def get_access_token
    if @user.spotify_cred.blank?
      auth_url = client.auth_code.authorize_url(redirect_uri: redirect_uri, response_type: 'code', client_id: ENV["spotify_client_id"], state: params[:session_code])
      render json: { success: false, url: auth_url} and return
    end
    creds = @user.spotify_cred
    token_hash = {
      access_token: creds.access_token,
      refresh_token: creds.refresh_token,
      expires_at: creds.expires_at.to_i
    }
    access_token = OAuth2::AccessToken.from_hash(client, token_hash)
    p "IN SPOTIFY PRINTING WOOOOOOOOOOOOOOOOOOOOOOOO"
    p access_token.expired?
    final_token = access_token.token
    final_expires_at = access_token.expires_at
    if access_token.expired?
      p final_token
      p "================="
      b = Base64.strict_encode64("#{ENV["spotify_client_id"]}:#{ENV["spotify_client_secret"]}")
      response = HTTParty.post(
        "https://accounts.spotify.com/api/token",
        :body => {:grant_type => "refresh_token",
                  :refresh_token => "#{access_token.refresh_token}"},
        :headers => {"Authorization" => "Basic #{b}"}
      )
      json_response = JSON.parse(response.body)
      final_token = json_response["access_token"]
      final_expires_at = (DateTime.now.to_time + json_response["expires_in"]).to_datetime
      p final_token 
      creds.update_attributes(access_token:  final_token, expires_at: final_expires_at )
    end
    render json: { success: true, access_token: final_token, expires_at: final_expires_at }
  end

  private
  def client
    @client ||= OAuth2::Client.new(ENV["spotify_client_id"], ENV["spotify_client_secret"], site: 'https://accounts.spotify.com', token_url: '/api/token')
  end

  def redirect_uri
    @redirect_uri ||= "#{ENV["backend_url"]}/spotify/get_hash"
  end
end
