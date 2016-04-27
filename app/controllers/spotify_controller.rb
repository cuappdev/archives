require 'net/https'
class SpotifyController < ApplicationController
  before_action :authorize, only: [:get_access_token]
  def get_hash
    code = params[:code]
    session_code = params[:state]
    p "WOOOOOOOOOOO"
    p params
    p code
    token = client.auth_code.get_token(params[:code], redirect_uri: redirect_uri).to_hash
    p token[:access_token]

    access_token = "Bearer " + token[:access_token]
    #access_token = token[:access_token]
    uri = URI.parse('https://api.spotify.com/v1/me')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Get.new(uri.request_uri, {'Content-Type' =>'application/json', 'Authorization' => access_token})
    response = http.request(request)
    res = JSON.parse(response.body)
    userId = res["id"]
    # @spotify_cred.update_username(userId)
    p "GETTING RESPONSE"
    p userId
    @spotify_cred = SpotifyCred.create(user_id: Session.where(code: session_code).limit(1).pluck(:user_id).first,
                                        access_token: token[:access_token],
                                        refresh_token: token[:refresh_token],
                                        expires_at: token[:expires_at],
                                        spotify_id: userId)

    data = {:name => "Icefishing Playlist"}
    access_token = @spotify_cred.access_token
    p " IN SPOTIFY SHIT"
    p access_token
    uri = URI.parse('https://api.spotify.com/v1/users/'+ username + '/playlists')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::POST.new(uri.request_uri, {'Content-Type' =>'application/json', Authorization => access_token})
    request.body = data.to_json
    response = http.request(request)
    res = JSON.parse(response.body)
    playlistId = res["id"]

    @spotify_cred.update_playlist(playlistId)
    redirect_to "#{ENV["icefishing-app-redirect"]}callback?access_token=#{token[:access_token]}&session_code=#{session_code}&expires_at=#{token[:expires_at]}"
  end
  def get_access_token
      p "in access token function"
    if @user.spotify_cred.blank?
        p "in access token function1"
      auth_url = client.auth_code.authorize_url(redirect_uri: redirect_uri, response_type: 'code', client_id: ENV["spotify_client_id"], state: params[:session_code])
      #auth_url="www.facebook.com"
      p auth_url
      render json: { success: false, url: auth_url} and return
    end
    p "in access token function2"
    creds = @user.spotify_cred
    token_hash = {
      access_token: creds.access_token,
      refresh_token: creds.refresh_token,
      expires_at: creds.expires_at.to_i
    }
    p "in access token function3"
    access_token = OAuth2::AccessToken.from_hash(client, token_hash)
    if access_token.expired?
        p "in access token function4"
      access_token.refresh!
      creds.update_attributes(access_token: access_token.token, refresh_token: access_token.refresh_token, expires_at: access_token.expires_at )
    end
    p "in access token function5"
    render json: { success: true, access_token: access_token.token, expires_at: access_token.expires_at }
  end

  private
  def client
    @client ||= OAuth2::Client.new(ENV["spotify_client_id"], ENV["spotify_client_secret"], site: 'https://accounts.spotify.com', token_url: '/api/token')
  end

  def redirect_uri
    @redirect_uri ||= "#{ENV["backend_url"]}/spotify/get_hash"
  end
end
