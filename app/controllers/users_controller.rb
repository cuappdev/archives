# == Schema Information
#
# Table name: users
#
#  id                                :integer          not null, primary key
#  name                              :string
#  hipster_score                     :integer          default(0)
#  caption                           :string
#  followers_count                   :integer          default(0)
#  location_id                       :integer
#  like_count                        :integer          default(0)
#  fbid                              :string
#  username                          :string
#  email                             :string
#  followings_count                  :integer          default(0)
#  created_at                        :datetime         not null
#  updated_at                        :datetime         not null
#  push_id                           :string
#  remote_push_notifications_enabled :boolean          default(TRUE)
#

class UsersController < ApplicationController

  before_action :authorize, only: [:index, :show, :create, :update, :likes, :posts, :user_suggestions, :followers, :following]


  def index
    if (params[:q].blank?)
      render json: { users: [] } and return
    end
    @users = User.where('username ILIKE :query', query: "#{ params[:q] }%")
    render json: { users: @users.map { |user| user.as_json(include_following: true, include_followers: true, user_id: @user.id) } }
  end


  def show
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

  def register_push 
    @param_user = User.find_by(id: params[:user_id])
    @param_user.update_push_id(params[:push_id])
    render json: { success: @param_user.push_id == params[:push_id] }
  end 

  def toggle_push
    @param_user = User.find_by(id: params[:id])
    @param_user.update_push_notifications_enabled(params[:enabled])
    render json: { success: @param_user.remote_push_notifications_enabled == params[:enabled] }
  end 

  def following
    @param_user = User.find(params[:id]) unless params[:id].blank?
    render json: {success: !@param_user.blank?, following: @param_user.following_list.map { |u| u.as_json(user_id: @user.id) }}
  end


  def followers
    @param_user = User.find(params[:id]) unless params[:id].blank?
    render json: {success: !@param_user.blank?, followers: @param_user.followers.map { |u| u.as_json(user_id: @user.id) }}
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
    session_code  = params[:session_code]
    username = params[:username]
    @user = User.find_by(username: username)
    if (@user)
        render json: {is_valid: false} and return
    else
        @session = Session.find_by(code: session_code)
        if (@session)
            @user = User.find_by(id: @session.user_id)
            if (!@user)
              render json: {status:401, message: "Invalid session code"} and return
            end
            bool_value = @user.update_username(username)
            @session.activate
            render json: {is_valid: bool_value} and return
        end
        render json: {is_valid: false}
    end
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
      comp = (-@user.mutual_following_count(a.id) <=> -@user.mutual_following_count(b.id))
      comp.zero? ? (-(a.like_count) <=> -(b.like_count)) : comp
    end
    data = sorted_data.slice(page * page_length, page_length).as_json(user_id: @user.id)
    render json: { users: data}
  end


  # Need to do
  def delete_user

  end

  private
  def user_params
    params.require(:user).permit(:name, :username)
    #params.require(:user).permit(:name)
  end

  def get_user
    @user = User.find(params[:id])
  end

end
