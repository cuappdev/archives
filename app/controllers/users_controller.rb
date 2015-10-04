class UsersController < ApplicationController

  before_action :authorize, only: [:show, :create, :update, :feed, :posts, :likes]
  
  def index
    @users = User.where('username ILIKE :query', query: "#{ params[:q] }%")
    render json: { users: @users.map { |user| user.as_json(include_following: true) } } 
  end

  def show
    p "======= User: #{@user.id}"
    render json: @user.as_json(include_followers: true, include_following: true)
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
    @posts = Post
      .where('user_id = ?', params[:id])
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
