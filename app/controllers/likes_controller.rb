class LikesController < ApplicationController
  before_action :authorize, only: [:create]
  def create
    unlike = params[:unlike]
    post_id = params[:post_id]
    unlike || unlike == 0 ? @user.unlike(post_id) : @user.like(post_id)
    render json: { success: true, liked: !@unlike }
  end
end
