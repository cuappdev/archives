class FeedController < ApplicationController
  def index
    render json: { posts: Post.where('created_at >= ?', Time.now.midnight) }
  end
end
