class SpotifyController < ApplicationController
  before_action :authorize, only: [:get_access_token]
  def get_url
    auth_url = client.auth_code.authorize_url(redirect_uri: redirect_uri, response_type: 'code', client_id: ENV["spotify_client_id"], state: params[:session_code])
    render json: { success: true, url: auth_url}
  end 
  def get_hash
    code = params[:code]
    session_code = params[:state]
    token = client.auth_code.get_token(params[:code], redirect_uri: redirect_uri).to_hash
    p '--------'
    p token
    p '--------'
    @spotify_cred = SpotifyCred.create(user_id: Session.where(code: session_code).limit(1).pluck(:user_id).first,access_token: token[:access_token], refresh_token: token[:refresh_token], expires_at: token[:expires_at])
    p @spotify_cred
    redirect_to "icefishing://access_token=#{token[:access_token]}"
    # token.token
    # token.refresh_token
    # token.expires_at
    # token = token.refresh!
    # TODO: Save token.to_h
    # TODO: Render
  end
  def get_access_token
    if @user.spotify_cred.blank?
      render json: { error: "You didnt authorize with spotify yet"}
      return
    end
    creds = @user.spotify_cred
    token_hash = {
      access_token: creds.access_token,
      refresh_token: creds.refresh_token,
      expires_at: creds.expires_at.to_i
    }
    access_token = OAuth2::AccessToken.from_hash(client, token_hash)
    access_token.refresh! if access_token.expired?
    render json: { access_token: access_token.token }
  end

  private
  def client
    @client ||= OAuth2::Client.new(ENV["spotify_client_id"], ENV["spotify_client_secret"], site: 'https://accounts.spotify.com', token_url: '/api/token')
  end

  def redirect_uri
    @redirect_uri ||= "#{ENV["backend_url"]}/spotify/get_hash"
  end
  # => "https://example.org/oauth/authorization?response_type=code&client_id=client_id&redirect_uri=http://localhost:8080/oauth2/callback"

  # response = token.get('/api/resource', :params => { 'query_foo' => 'bar' })
  # response.class.name
  # => OAuth2::Response
end
