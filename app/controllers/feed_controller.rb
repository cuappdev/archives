class FeedController < ApplicationController
  # before_action :authorize
  def index
    render json: { posts: Post.where('created_at >= ?', Time.now.midnight) }
  end
end
