class FeedController < ApplicationController
  before_action :authorize, only: [:index]
  def index
    queryResult = Post.joins("INNER JOIN followings ON (followings.follower_id = #{@user.id} AND posts.user_id = followings.followed_id) WHERE posts.created_at >= NOW() - '1 day'::INTERVAL ORDER BY posts.created_at DESC").select("posts.*");
    posts = queryResult.map { |post| post.as_json(id: @user.id) }
    render json: { "posts": posts}
  end
end
