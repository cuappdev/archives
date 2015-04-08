class SessionsController < ApplicationController
  def create
    @user = User.find_or_create_by(email: params[:user][:email])
    if @user
      # FIXME: Don't need to create a new session every time, update existing if possible
      @session = Session.create(user_id: @user.id)
    else
      @session = nil
    end
    render json: { success: !@session.blank?, user: @user, session: @session }
  end 
end
