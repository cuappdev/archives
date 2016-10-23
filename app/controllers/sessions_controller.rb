class SessionsController < ApplicationController
  require 'http_helper'
  def create
    
    #check for an existing user with this fbid
    user_token = params[:user][:usertoken]
    url = FACEBOOK_USER_URL + user_token
    res = get({}, {}, url)
    fbid = res["id"]

    #check for invalid user token
    if fbid.nil?
        render json: {success: false, status: 401, error: "invalid or expired user token"}
        return
    end

    @user = User.find_by(fbid: fbid)
    if !(@user)
        @user = User.create!(user_params(fbid))
    end
    @session = Session.find_or_create_by!(user_id: @user.id)
    @session.activate
    render json: { success: !@session.blank?, user: @user, session: @session }
  end

  def logout
    @session = Session.find_by(code:params[:session_code])
    if @session
      @session.disable
    end
    render json: { success: !@session.blank?, session: @session}
  end

  private
  def user_params(fbid)
    params.require(:user).permit(:email, :name, :username).merge(fbid:fbid, username:fbid)
  end
end
