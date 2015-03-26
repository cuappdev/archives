class UsersController < ApplicationController

  before_action :get_user, only: [:show]
  
  def index
    respond_to do |format|
      format.html { render text: 'This is HTML' }
      format.json { render json: 'This is JSON' }
    end
  end

  def show
    render json: @user
  end

  def create
    @user = User.create(user_params)
    render json: { success: !@user.blank? }
  end

  private
  def user_params
    params.require(:user).permit(:name, :caption)
  end
  
  def get_user
    @user = User.find(params[:id])
  end
end
