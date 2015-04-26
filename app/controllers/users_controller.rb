class UsersController < ApplicationController

  before_action :authorize, only: [:show, :create, :update, :feed, :posts]
  
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

  def update
    @user = User.update_attributes(user_params)
    render json: { user: @user }
  end

  def feed
    followers_ids = Following.where(follower_id: params[:id]).pluck(:followed_id)
    @posts = Post
      .where(user_id: followers_ids).includes(:user)
    render json: { posts: @posts }
  end

  def posts
    @posts = Post
      .where('created_at >= ?', Time.now.midnight)
      .where(user_id: @user.id).includes(:user)
    render json: @posts
  end

  def valid_username
    render json: { is_valid: !User.exists?(username: params[:username]) }
  end

  private
  def user_params
    params.require(:user).permit(:name, :username)
  end
  
  def get_user
    @user = User.find(params[:id])
  end
end
