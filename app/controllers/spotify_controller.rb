class SpotifyController < ApplicationController
  before_action :authorize, only: [:get_access_token]
  def get_hash
    code = params[:code]
    session_code = params[:state]
    token = client.auth_code.get_token(params[:code], redirect_uri: redirect_uri).to_hash
    @spotify_cred = SpotifyCred.create(user_id: Session.where(code: session_code).limit(1).pluck(:user_id).first,access_token: token[:access_token], refresh_token: token[:refresh_token], expires_at: token[:expires_at])
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
    if access_token.expired?
      access_token.refresh! 
      creds.update_attributes(access_token: access_token.token, refresh_token: access_token.refresh_token, expires_at: access_token.expires_at )
    end
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
