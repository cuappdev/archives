class UsersController < ApplicationController

  before_action :authorize, only: [:show, :create, :update, :likes, :posts, :user_suggestions]
  def index
    @users = User.where('username ILIKE :query', query: "#{ params[:q] }%")
    render json: { users: @users.map { |user| user.as_json(include_following: true, include_followers: true) } } 
  end

  def show
    p '====='
    p @user.id
    p '====='
    render json: User.find(params[:id]).as_json(user_id: @user.id, include_followers: true, include_following: true)
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
    render json: { posts: @posts.map { |post| post.as_json(id: @user.id) } }
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

  # User suggestions
  def user_suggestions
    all_user_ids = (User.all.pluck(:id)-@user.followings_ids)-[(@user.id)]
    page_length = params[:l].blank? ? 5 : (params[:l]).to_i
    page = params[:p].blank? ? 0 : (params[:p]).to_i
    sorted_data = User.where('id in (?)', all_user_ids).sort do |a,b|
      comp = (-@user.mutual_friends(a.id) <=> -@user.mutual_friends(b.id))
      comp.zero? ? (-(a.like_count) <=> -(b.like_count)) : comp
    end
    data = sorted_data.slice(page * page_length, page_length).as_json
    render json: { users: data}
  end
  # Need to do
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
