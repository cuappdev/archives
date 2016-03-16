class SessionsController < ApplicationController
  def create
    #check for an existing user with this fbid
    @user = User.find_or_create_by(user_params)
    @session = Session.find_or_create_by(user_id: @user.id)
    render json: { success: !@session.blank?, user: @user, session: @session }
  end

  private
  def user_params
    user_token = params[:user][:usertoken]
    uri = URI.parse('https://graph.facebook.com/me?fields=id&access_token='+ user_token)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)
    res = JSON.parse(response.body)
    fbid = res["id"]
    params.require(:user).permit(:email, :name, :username).merge(fbid: fbid)
  end
end
