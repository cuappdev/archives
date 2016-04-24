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
  def create
    #check for an existing user with this fbid
    user_token = params[:user][:usertoken]
    uri = URI.parse('https://graph.facebook.com/me?fields=id&access_token='+ user_token)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)
    res = JSON.parse(response.body)
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
    params.require(:user).permit(:email, :name, :username).merge(fbid:fbid)
  end
end
