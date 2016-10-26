require 'rails_helper'

RSpec.describe FollowingsController, type: :controller do

end

"""
# == Schema Information
#
# Table name: followings
#
#  id          :integer          not null, primary key
#  follower_id :integer
#  followed_id :integer
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

class FollowingsController < ApplicationController
  before_action :authorize, only: [:create]
  include FollowingsHelper
  def create
    # Is following?
    follow_bool = (params[:unfollow] == "0")
    # following id
    followed_id = params[:followed_id]
    # cant follow yourself
    if @user.id == followed_id
      render json: { success: false, follow: follow_bool}
    end
    # success value on the follow or unfollow
    success_val = (follow_bool ? @user.follow(followed_id) : @user.unfollow(followed_id))
    # if successful update the mutual friends by passing in whether it was follow,
    # the user who followed, and the follower
    update_mutual_friends(follow_bool, @user.id, followed_id) if success_val
    render json: { success: success_val, follow: follow_bool }
  end
end
"""
