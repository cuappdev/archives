class SessionsController < ApplicationController
  def create
    #####ADD facebook logic here#######
    p "GOT TO THE FUNCTION WOT WOOT"
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
    check for an existing user with this fbid
    @user = User.find_by(fbid: fbid)
    if @user
      @session = Session.find_by(user_id:@user.id)
    else
      p params 
      @user = User.create





    ###query fbid and get user info from facebook
    ##query username--if there is one, return the existing session
    ##isnot, create a new session and give it to them 

    @user = User.find_by(email: params[:user][:email])
    if @user
      # FIXME: Don't need to create a new session every time, update existing if possible--column isActive
      @session = Session.create(user_id: @user.id)
    else
      @user = User.create(user_params)
      @session = Session.create(user_id: @user.id)
    end
    render json: { success: !@session.blank?, user: @user, session: @session }
  end

  private
  def user_params
    params.require(:user, :fbid).permit(:email, :name, :username)
  end
end
