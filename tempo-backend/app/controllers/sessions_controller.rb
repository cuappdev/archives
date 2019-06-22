# == Schema Information
#
# Table name: sessions
#
#  id         :integer          not null, primary key
#  user_id    :integer
#  code       :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  is_active  :boolean
#

class SessionsController < ApplicationController
  include HttpHelper
  def create
    #check for an existing user with this fbid
    user_token = params[:user][:usertoken]
    url = FACEBOOK_USER_URL + user_token
    res = get({}, {"nothing": true}.to_json, url)
    p res
    fbid = res["id"]

    #check for invalid user token
    if fbid.nil?
        render json: {success: false, status: 401, error: "invalid or expired user token"}
        return
    end
    @user = User.find_by(fbid: fbid)
    new_user = false
    if !(@user)
        @user = User.new(user_params(fbid: fbid))
        @user.default_values
        @user.save!
        p @user
        new_user = true
    end
    @session = Session.find_or_create_by!(user_id: @user.id)
    @session.activate
    render json: { success: !@session.blank?, user: @user, session: @session, new_user: new_user}
  end



  def logout
    @session = Session.find_by(code:params[:session_code])
    if @session
      @session.disable
    end
    render json: { success: !@session.blank?, session: @session}
  end

  private
  def user_params(extra={})
    params.require(:user).permit(:email, :name).merge(extra)
  end
end
