class SessionsController < ApplicationController
  def create
    #####ADD facebook logic here#######
    params.require(:usertoken)
    user_token = params[:usertoken]
    p user_token
    p "**************************"
    uri = URI.parse('https://graph.facebook.com/me?fields=id&access_token='+ user_token)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE

    request = Net::HTTP::Get.new(uri.request_uri)

    response = http.request(request)
    p response.body
    res = JSON.parse(response.body)
    p res;
    p res["id"]
    fbid = res["id"]
    #check for an existing user with this fbid
    @user = User.find_by(fbid: fbid)
    if @user
      @session = Session.find_by(user_id:@user.id)
    else
      #@user = User.create(email: params[:user][:email], fbid: fbid)
      @user = User.create(user_params, fbid)
      @session = Session.create(user_id: @user.id)
    end
    render json: { success: !@session.blank?, user: @user, session: @session }
  end

  private
  def user_params
    params.require(:user, :fbid).permit(:email, :name, :username)
  end
end
