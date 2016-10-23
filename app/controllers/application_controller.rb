class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :null_session

  def authorize
    head(401) and return false if params[:session_code].blank?
    @session = Session.find_by_code(params[:session_code])
    if @session.blank?
      render json: { success: false, error: 'Unauthorized' }, status: :unauthorized
      return false
    end
    @user = @session.user
  end
  SPOTIFY_URL = 'https://api.spotify.com/v1/'
  FACEBOOK_USER_URL = 'https://graph.facebook.com/me?fields=id&access_token='
end
