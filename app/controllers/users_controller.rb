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

  def feed
    followers_ids = Following.where(follower_id: params[:id]).pluck(:followed_id)
    @posts = Post
      .where('created_at >= ?', Time.now.midnight)
      .where(user_id: followers_ids).includes(:user)
    render json: @posts
  end

  private
  def user_params
    params.require(:user).permit(:name, :caption)
  end
  
  def get_user
    @user = User.find(params[:id])
  end
end
