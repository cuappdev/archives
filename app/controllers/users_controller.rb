class UsersController < ApplicationController

  before_action :authorize, only: [:show, :create, :update, :likes]
  
  def index
    @users = User.where('username ILIKE :query', query: "#{ params[:q] }%")
    render json: { users: @users.map { |user| user.as_json(include_following: true, include_followers: true) } } 
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
    @user = @user.update_attributes(user_params) # update_attributes returns result of #save
    success = @user # #save is truthy if the model is valid and gets committed, falsey otherwise
    status = success ? :ok : :bad_request
    render json: { success: success, user: @user.as_json(include_followers: true) }, status: status
  end

  def following
    @user = User.find(params[:id]) unless params[:id].blank?
    render json: {success: !@user.blank?, following: @user.following_list}
  end

  def followers
    @user = User.find(params[:id]) unless params[:id].blank?
    render json: {success: !@user.blank?, followers: @user.followers}
  end

  def posts
    @posts = Post
      .where('user_id = ?', params[:id])
      .order('created_at DESC')
    render json: { posts: @posts.map { |post| post.as_json(id: params[:id]) } }
  end

  def likes
    @user = User.find(params[:id])
    @likes = @user.likes.includes(:post)
    @songs = @likes.map{ |like| like.post.songs.first }.uniq
    render json: { songs: @songs }
  end

  def valid_username
    render json: { is_valid: !User.where('username ILIKE (?)', params[:username]).exists? }
  end
  def valid_fbid
    render json: { is_valid: !User.exists?(fbid: params[:fbid]) }
  end

  def delete_user
    
  end
  private
  def user_params
    params.require(:user).permit(:name, :username)
  end
  
  def get_user
    @user = User.find(params[:id])
  end
end
