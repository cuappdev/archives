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

  private
  def get_user
    @user = User.find(params[:id])
  end
end
