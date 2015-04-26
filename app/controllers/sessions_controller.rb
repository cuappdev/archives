class SessionsController < ApplicationController
  def create
    @user = User.find_by(email: params[:user][:email])
    if @user
      # FIXME: Don't need to create a new session every time, update existing if possible
      @session = Session.create(user_id: @user.id)
    else
      @user = User.create(user_params)
      @session = Session.find_by(user_id: @user.id)
    end
    render json: { success: !@session.blank?, user: @user, session: @session }
  end

  private
  def user_params
    params.require(:user).permit(:fbid, :email, :name, :username)
  end
end
