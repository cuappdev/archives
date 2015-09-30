class UsersController < ApplicationController

  before_action :authorize, only: [:show, :create, :update, :feed, :posts, :likes]
  
  def index
    @users = User.where('username ILIKE :query', query: "#{ params[:q] }%")
    respond_to do |format|
      format.html { render text: 'This is HTML' }
      format.json { render json: { users: @users } }
    end
  end

  def show
    render json: @user.as_json(include_followers: true)
  end

  def create
    @user = User.create(user_params)
    render json: { success: !@user.blank? }
  end

  def update
    @user = @user.update_attributes(user_params)
    render json: { user: @user.as_json(include_followers: true) }
  end

  def feed
    followings_ids = User.find(params[:id]).followings_ids
    @posts = Post
      .where('user_id IN (?)', followings_ids)
      .where('created_at >= ?', Time.now.midnight)
      .order('created_at DESC')
    render json: { posts: @posts }
  end

  def posts
    @posts = Post
      .where(user_id: @user.id).includes(:user)
      .where('created_at >= ?', Time.now.midnight)
    render json: @posts
  end

  def likes
    @user = User.find(params[:id])
    @likes = @user.likes.includes(:post)
    @songs = @likes.map{ |like| like.post.songs.first }.uniq
    render json: { songs: @songs }
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
